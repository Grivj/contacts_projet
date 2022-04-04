import os

from AgreementGenerator import AgreementGenerator
from flask import send_from_directory
from flask_restful import Resource, abort
from models.Contact import Contact


class GenerateAgreement(Resource):
    def get(self, id: int):
        contact = Contact.query.filter_by(id=id).first()
        if contact is None:
            abort(404, message=f"Contact {id} doesn't exist")
        if contact.company is None or contact.siren is None:
            abort(404, message=f"Contact {id} doesn't have a company or a siren number")

        agreement = AgreementGenerator(
            contact.id, contact.name, contact.company, contact.siren
        )
        agreement.generate()

        return "Agreement generated", 200


class DownloadAgreement(Resource):
    def get(self, id: int):
        contact = Contact.query.filter_by(id=id).first()
        if contact is None:
            abort(404, message=f"Contact {id} doesn't exist.")
        if contact.company is None or contact.siren is None:
            abort(
                404, message=f"Contact {id} doesn't have a company or a siren number."
            )

        agreement = AgreementGenerator(
            contact.id, contact.name, contact.company, contact.siren
        )
        if not os.path.isfile(f"/bpa/{contact.siren}.pdf"):
            agreement.generate()

        return send_from_directory(
            directory=agreement.dir,
            path=agreement.filename,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"{contact.siren}_bon_pour_accord.pdf",
        )
