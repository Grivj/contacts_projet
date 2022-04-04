from flask import Response, request
from flask_restful import Resource, abort, marshal_with
from models.Contact import Contact, resource_fields


class Tunnel(Resource):
    @marshal_with(resource_fields)
    def get(self):
        contact = Contact.query.filter_by(called=False).first()
        if not contact:
            return {"message": "No more contacts to call"}, 404
        return contact, 200

    @marshal_with(resource_fields)
    def put(self, id: int) -> Contact:
        contact = Contact.query.filter_by(id=id).first()
        if contact is None:
            abort(404, message=f"Contact {id} doesn't exist")
        data = request.get_json()
        contact.update(data)
        return contact, 200
