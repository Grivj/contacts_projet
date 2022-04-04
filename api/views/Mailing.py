import os

from AgreementGenerator import AgreementGenerator
from flask import send_from_directory
from flask_mail import Mail, Message
from flask_restful import Resource, abort
from mail import mail
from models.Contact import Contact

ADDRESS = "jordan.testing.ayomi@gmail.com"
PASSWORD = "AYOMItestingEMAIL"


class Mailing(Resource):
    def get(self, id: int):
        contact = Contact.query.filter_by(id=id).first()
        if contact is None:
            abort(404, message=f"Contact {id} doesn't exist")
        if contact.company is None or contact.siren is None:
            abort(
                404, message=f"Contact {id} doesn't have a company or a siren number."
            )
        if contact.email is None:
            abort(404, message=f"Contact {id} doesn't have an email address.")

        # since we are mailing the agreement pdf, look for it on the server and
        # create it if not present.
        agreement = AgreementGenerator(
            contact.id, contact.name, contact.company, contact.siren
        )
        if not os.path.isfile(f"/bpa/{contact.siren}.pdf"):
            agreement.generate()

        msg = Message("Hello", sender=ADDRESS, recipients=[contact.email])
        msg.body = "Please find your agreement contract."

        # join the pdf in the mail
        msg.attach(
            filename="bon_pour_accord.pdf",
            content_type="application/pdf",
            data=open(f"/bpa/{contact.siren}.pdf", "rb").read(),
        )
        mail.send(msg)

        return "Mail sent", 200
