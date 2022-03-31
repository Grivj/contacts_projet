from flask import Flask, Response, jsonify, make_response, request
from flask_restful import Api, Resource, abort, reqparse

app = Flask(__name__)
api = Api(app)


FAKE_DATABASE = [
    {
        "id": 1,
        "firstName": "John",
        "lastName": "Doe",
        "phoneNumber": "+33643014673",
        "company": "Apple",
    },
    {
        "id": 2,
        "firstName": "Jane",
        "lastName": "Doe",
        "phoneNumber": "+33643014673",
        "company": "Google",
    },
    {
        "id": 3,
        "firstName": "Jack",
        "lastName": "Doe",
        "phoneNumber": "+33643014673",
        "company": "LinkedIn",
    },
    {
        "id": 4,
        "firstName": "Joe",
        "lastName": "Doe",
        "phoneNumber": "+33643014673",
        "company": "Google",
    },
    {
        "id": 5,
        "firstName": "Jack",
        "lastName": "Doe",
        "phoneNumber": "+33643014673",
        "company": "Google",
    },
    {
        "id": 6,
        "firstName": "Joe",
        "lastName": "Doe",
        "phoneNumber": "+33643014673",
        "company": "Google",
    },
    {
        "id": 7,
        "firstName": "Jack",
        "lastName": "Doe",
        "phoneNumber": "+33643014673",
        "company": "Google",
    },
    {
        "id": 8,
        "firstName": "Joe",
        "lastName": "Doe",
        "phoneNumber": "+33643014673",
        "company": "Google",
    },
    {
        "id": 9,
        "firstName": "Jack",
        "lastName": "Doe",
        "phoneNumber": "+33643014673",
        "company": "Google",
    },
    {
        "id": 10,
        "firstName": "Joe",
        "lastName": "Doe",
        "phoneNumber": "+33643014673",
        "company": "Google",
    },
]

parser = reqparse.RequestParser()
parser.add_argument("firstName", type=str, help="First name of the contact")
parser.add_argument("lastName", type=str, help="Last name of the contact")
parser.add_argument("phoneNumber", type=str, help="Phone number of the contact")


class Index(Resource):
    def get(self):
        return "Hello", 200


def get_contact_index_by_id_if_exists(contact_id: int):
    for idx, contact in enumerate(FAKE_DATABASE):
        if contact["id"] == contact_id:
            return idx
    abort(404, message=f"Contact {contact_id} doesn't exist")


class Contact(Resource):
    def get(self, contact_id: int) -> dict:
        contact_idx = get_contact_index_by_id_if_exists(contact_id)
        return FAKE_DATABASE[contact_idx], 200

    def delete(self, contact_id: int):
        contact_idx = get_contact_index_by_id_if_exists(contact_id)
        del FAKE_DATABASE[contact_idx]
        return "", 204

    def put(self, contact_id: int):
        contact_idx = get_contact_index_by_id_if_exists(contact_id)
        contact = FAKE_DATABASE[contact_idx]
        content = request.json
        for key in content:
            if key == "id":
                continue
            contact[contact_idx][key] = content[key]
        return FAKE_DATABASE[contact_idx], 201


class ContactList(Resource):
    def get(self):
        return FAKE_DATABASE

    def post(self):
        data = request.json
        data["id"] = max(contact["id"] for contact in FAKE_DATABASE) + 1
        FAKE_DATABASE.append(data)
        return data, 201


api.add_resource(Index, "/")
api.add_resource(ContactList, "/contacts")
api.add_resource(Contact, "/contacts/<int:contact_id>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
