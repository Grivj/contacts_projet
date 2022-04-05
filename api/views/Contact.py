from flask import Response, request
from flask_restful import Resource, marshal_with
from models.Contact import Contact, get_contact_by_id_or_abort, resource_fields


class ContactInfo(Resource):
    """
    Resource that contains information about a single contact, associated with
    diverse HTTP methods.
    """
    @marshal_with(resource_fields)
    def get(self, id: int) -> Contact:
        return get_contact_by_id_or_abort(id), 200

    @marshal_with(resource_fields)
    def put(self, id: int) -> Contact:
        contact = get_contact_by_id_or_abort(id)
        data = request.get_json()
        contact.update(data)
        return contact, 200

    def delete(self, id: int) -> Response:
        contact = get_contact_by_id_or_abort(id)
        contact.delete()
        return "", 204


class ContactList(Resource):
    """
    Resource that contains information about all the contacts.
    Possibility to create a new contact.
    """
    @marshal_with(resource_fields)
    def post(self):
        data = request.get_json()
        contact = Contact(**data)
        contact.create()
        return contact, 201

    @marshal_with(resource_fields)
    def get(self):
        return Contact.query.all(), 200
