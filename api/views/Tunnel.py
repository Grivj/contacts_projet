from flask import Response, request
from flask_restful import Resource, abort
from models.Contact import Contact


class Tunnel(Resource):
    def get(self):
        # get the first not called contact
        contact = Contact.query.filter_by(called=False).first()._serialize()
        if not contact:
            return {"message": "No more contacts to call"}, 404
        return contact, 200

    def put(self, id: int) -> Contact:
        contact = Contact.query.filter_by(id=id).first()
        if contact is None:
            abort(404, message=f"Contact {id} doesn't exist")
        data = request.get_json()
        contact.update(data)
        return contact._serialize(), 200
