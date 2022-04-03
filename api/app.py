import os

import requests
from faker import Faker
from flask import Flask, Response, request
from flask_restful import Api, Resource, abort
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}".format(
    os.getenv("DB_USER", "root"),
    os.getenv("DB_PASSWORD", "root"),
    os.getenv("DB_HOST", "mysql"),
    os.getenv("DB_NAME", "db"),
)
engine = create_engine(
    app.config["SQLALCHEMY_DATABASE_URI"], pool_recycle=2000, pool_size=20
)
sessionmaker(bind=engine)


db = SQLAlchemy(app)


class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=True)
    name = db.Column(db.String(80), nullable=True)
    phone_number = db.Column(db.String(10), nullable=True)
    siren = db.Column(db.String(14), nullable=True)
    company = db.Column(db.String(80), nullable=True)
    called = db.Column(db.Boolean, default=False, nullable=True)

    def _serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    def update(self, updated_contact: dict):
        for column in self.__table__.columns.keys():
            if column in updated_contact:
                setattr(self, column, updated_contact[column])

        db.session.add(self)
        db.session.commit()


db.create_all()

# creates dummy Contacts before the first query and if no Contacts are in the database


# Creates dummy Contacts if none exist already.
if db.session.query(Contact).count() == 0:
    faker = Faker("fr_FR")
    fake_contacts = [
        Contact(
            name=faker.name(),
            phone_number="0643014673",
            email=faker.email(),
            siren="838170918"
            # company=faker.company(),
        )
        for _ in range(10)
    ]
    db.session.add_all(fake_contacts)
    db.session.commit()


class Index(Resource):
    def get(self):
        return "Hello", 200


class Tunnel(Resource):
    def get(self):
        # get the first not called contact
        contact = db.session.query(Contact).filter_by(called=False).first()._serialize()
        if not contact:
            return {"message": "No more contacts to call"}, 404
        return contact, 200


class TunnelUpdate(Resource):
    def put(self, id: int) -> Contact:
        contact = db.session.query(Contact).filter_by(id=id).first()
        if contact is None:
            abort(404, message=f"Contact {id} doesn't exist")
        data = request.get_json()
        contact.update(data)
        db.session.commit()
        return contact._serialize(), 200


class ContactInfo(Resource):
    def get(self, id: int) -> Contact:
        """
        Retrieve the contact in the database by id.
        If the contact is not found, abort with a 404 error.
        Args:
            id (int): contact id

        Returns:
            dict: Serialized contact
        """
        contact = db.session.query(Contact).filter_by(id=id).first()
        if contact is None:
            abort(404, message=f"Contact {id} doesn't exist")
        return contact._serialize(), 200

    # Get the modified contact from request then modify in database if contact is found
    def put(self, id: int) -> Contact:
        """
        Update the contact in the database by id.
        If the contact is not found, abort with a 404 error.
        Args:
            id (int): contact id
            request (dict): request data

        Returns:
            dict: Serialized contact
        """
        contact = db.session.query(Contact).filter_by(id=id).first()
        if contact is None:
            abort(404, message=f"Contact {id} doesn't exist")
        data = request.get_json()
        contact.update(data)
        db.session.commit()
        return contact._serialize(), 200

    # Delete the contact by id; if the contact is not found, abort with a 404 error.
    def delete(self, id: int) -> Response:
        """
        Delete the contact in the database by id.
        If the contact is not found, abort with a 404 error.
        Args:
            id (int): contact id
        """
        contact = db.session.query(Contact).filter_by(id=id).first()
        if contact is None:
            abort(404, message=f"Contact {id} doesn't exist")
        db.session.delete(contact)
        db.session.commit()
        return "", 204


class ContactList(Resource):
    def post(self):
        data = request.get_json()
        contact = Contact(**data)
        db.session.add(contact)
        db.session.commit()
        db.session.flush()
        return contact._serialize(), 201

    def get(self):
        contacts = Contact.query.all()

        return [contact._serialize() for contact in contacts], 200


class ScrapperCompanyName(Resource):
    def get(self, siren: str):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        driver = webdriver.Remote(
            command_executor="http://172.18.0.3:4444/wd/hub",
            options=chrome_options,
        )
        driver.get("https://www.societe.com")
        search_form = driver.find_element(By.NAME, "champs")
        search_form.send_keys(siren)
        search_form.submit()

        try:
            company_name = driver.find_element(By.ID, "identite_deno").text
            driver.quit()
            return company_name, 200

        except NoSuchElementException:
            driver.quit()
            abort(404, message=f"Company name with SIREN number: {siren} was not found")


api.add_resource(Index, "/")
api.add_resource(ContactList, "/contacts")
api.add_resource(ContactInfo, "/contacts/<int:id>")
api.add_resource(Tunnel, "/tunnel")
api.add_resource(TunnelUpdate, "/tunnel/<int:id>")
api.add_resource(ScrapperCompanyName, "/scrapper_company_name/<string:siren>")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
