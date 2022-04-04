import os

from AgreementGenerator import AgreementGenerator
from flask_mail import Message
from flask_restful import Resource, abort
from mail import mail
from models.Contact import get_contact_by_id_or_abort, if_empty_company_or_siren_abort

ADDRESS = "jordan.testing.ayomi@gmail.com"
PASSWORD = "AYOMItestingEMAIL"


class Mailing(Resource):
    def get(self, id: int):
        contact = get_contact_by_id_or_abort(id)
        if_empty_company_or_siren_abort(contact)
        if not contact.email:
            abort(404, message=f"Contact {id} doesn't have an email address.")

        # since we are mailing the agreement pdf, look for it on the server and
        # create it if not present.
        agreement = AgreementGenerator(
            contact.id, contact.name, contact.company, contact.siren
        )
        if not agreement.is_already_exists:
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
