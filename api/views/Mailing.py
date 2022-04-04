import smtplib
import ssl

from flask import send_from_directory
from flask_restful import Resource, abort
from models.Contact import Contact

ADDRESS = "jordan.testing.ayomi@gmail.com"
PASSWORD = "AYOMItestingEMAIL"


class Mailing(Resource):
    contact = Contact.query.filter_by(id=id).first()
    if contact is None:
        abort(404, message=f"Contact {id} doesn't exist")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(ADDRESS, PASSWORD)
        print(server, flush=True)
