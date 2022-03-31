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
    email = db.Column(db.String(80))
    name = db.Column(db.String(80))
    phone_number = db.Column(db.Integer)
    siren = db.Column(db.Integer())
    company = db.Column(db.String(80))
    called = db.Column(db.Boolean, default=False)

    def _serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}


db.create_all()

faker = Faker("fr_FR")
fake_contacts = [
    Contact(name=faker.name(), phone_number="0643014673", email=faker.email())
    for _ in range(100)
]
db.session.add_all(fake_contacts)
db.session.commit()


class Index(Resource):
    def get(self):
        return "Hello", 200


# def get_contact_index_by_id_if_exists(contact_id: int):
#     for idx, contact in enumerate(FAKE_DATABASE):
#         if contact["id"] == contact_id:
#             return idx
#     abort(404, message=f"Contact {contact_id} doesn't exist")


# class Contact(Resource):
#     def get(self, contact_id: int) -> dict:
#         contact_idx = get_contact_index_by_id_if_exists(contact_id)
#         return FAKE_DATABASE[contact_idx], 200

#     def delete(self, contact_id: int):
#         contact_idx = get_contact_index_by_id_if_exists(contact_id)
#         del FAKE_DATABASE[contact_idx]
#         return "", 204

#     def put(self, contact_id: int):
#         contact_idx = get_contact_index_by_id_if_exists(contact_id)
#         content = json.loads(request.json)
#         print(content)
#         for key in content.keys():
#             print(key)
#             if key == "id":
#                 continue
#             FAKE_DATABASE[contact_idx][key] = content[key]
#         return FAKE_DATABASE[contact_idx], 201


class ContactList(Resource):
    # def get(self):
    # return FAKE_DATABASE

    # def post(self):
    #     data = request.json
    #     data["id"] = max(contact["id"] for contact in FAKE_DATABASE) + 1
    #     FAKE_DATABASE.append(data)
    #     return data, 201

    def get(self):
        contacts = Contact.query.all()

        return [contact._serialize() for contact in contacts], 200


# ADDING ROUTES
api.add_resource(Index, "/")
api.add_resource(ContactList, "/contacts")
# api.add_resource(Contact, "/contacts/<int:contact_id>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
