import json
import os

from faker import Faker
from flask import Flask, Response, jsonify, make_response, request
from flask_restful import Api, Resource, abort, reqparse
from flask_sqlalchemy import SQLAlchemy
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


# Creates dummy Contacts if none exist already.
if db.session.query(Contact).count() == 0:
    faker = Faker("fr_FR")
    fake_contacts = [
        Contact(
            name=faker.name(),
            phone_number="0643014673",
            email=faker.email(),
            company=faker.company(),
        )
        for _ in range(10)
    ]
    db.session.add_all(fake_contacts)
    db.session.commit()


# parser = reqparse.RequestParser()
# parser.add_argument("name", type=str)
# parser.add_argument("email", type=str)
# parser.add_argument("phone_number", type=int)
# parser.add_argument("siren", type=str)
# parser.add_argument("company", type=str)
# parser.add_argument("called", type=bool)


class Index(Resource):
    def get(self):
        return "Hello", 200


# def get_contact_index_by_id_if_exists(contact_id: int):
#     for idx, contact in enumerate(FAKE_DATABASE):
#         if contact["id"] == contact_id:
#             return idx
#     abort(404, message=f"Contact {contact_id} doesn't exist")


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
        data = request.json
        print(json.loads(data), flush=True)
        # contact.update(updated_contact)
        # db.session.commit()
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
    # def get(self):
    # return FAKE_DATABASE

    def post(self):
        data = request.get_json()
        contact = Contact(**data)
        db.session.add(contact)
        db.session.commit()
        db.session.flush()
        print(data, flush=True)
        return contact._serialize(), 201

    def get(self):
        contacts = Contact.query.all()

        return [contact._serialize() for contact in contacts], 200


# ADDING ROUTES
api.add_resource(Index, "/")
api.add_resource(ContactList, "/contacts")
api.add_resource(ContactInfo, "/contacts/<int:id>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
