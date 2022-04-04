from flask import Response, request
from flask_restful import Resource, abort, marshal_with
from models.Contact import Contact, resource_fields


class ContactInfo(Resource):
    @marshal_with(resource_fields)
    def get(self, id: int) -> Contact:
        contact = Contact.query.filter_by(id=id).first()
        if contact is None:
            abort(404, message=f"Contact {id} doesn't exist")
        return contact, 200

    @marshal_with(resource_fields)
    def put(self, id: int) -> Contact:
        contact = Contact.query.filter_by(id=id).first()
        if contact is None:
            abort(404, message=f"Contact {id} doesn't exist")
        data = request.get_json()
        contact.update(data)
        return contact, 200

    def delete(self, id: int) -> Response:
        contact = Contact.query.filter_by(id=id).first()
        if contact is None:
            abort(404, message=f"Contact {id} doesn't exist")
        contact.delete()
        return "", 204


class ContactList(Resource):
    @marshal_with(resource_fields)
    def post(self):
        data = request.get_json()
        contact = Contact(**data)
        contact.create()
        return contact, 201

    @marshal_with(resource_fields)
    def get(self):
        return Contact.query.all(), 200
