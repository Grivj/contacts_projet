from flask import Response, request
from flask_restful import Resource, abort
from models.Contact import Contact


class ContactInfo(Resource):
    def get(self, id: int) -> Contact:
        contact = Contact.query.filter_by(id=id).first()
        if contact is None:
            abort(404, message=f"Contact {id} doesn't exist")
        return contact._serialize(), 200

    def put(self, id: int) -> Contact:
        contact = Contact.query.filter_by(id=id).first()
        if contact is None:
            abort(404, message=f"Contact {id} doesn't exist")
        data = request.get_json()
        contact.update(data)
        return contact._serialize(), 200

    def delete(self, id: int) -> Response:
        contact = Contact.query.filter_by(id=id).first()
        if contact is None:
            abort(404, message=f"Contact {id} doesn't exist")
        contact.delete()
        return "", 204


class ContactList(Resource):
    def post(self):
        data = request.get_json()
        contact = Contact(**data)
        contact.create()
        return contact._serialize(), 201

    def get(self):
        contacts = Contact.query.all()

        return [contact._serialize() for contact in contacts], 200
