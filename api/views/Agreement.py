from AgreementGenerator import AgreementGenerator
from flask import send_from_directory
from flask_restful import Resource
from models.Contact import get_contact_by_id_or_abort, if_empty_company_or_siren_abort


class GenerateAgreement(Resource):
    def get(self, id: int):
        contact = get_contact_by_id_or_abort(id)
        if_empty_company_or_siren_abort(contact)

        agreement = AgreementGenerator(
            contact.id, contact.name, contact.company, contact.siren
        )
        agreement.generate()

        return "Agreement generated", 200


class DownloadAgreement(Resource):
    def get(self, id: int):
        contact = get_contact_by_id_or_abort(id)
        if_empty_company_or_siren_abort(contact)

        agreement = AgreementGenerator(
            contact.id, contact.name, contact.company, contact.siren
        )
        if not agreement.is_already_exists:
            agreement.generate()

        return send_from_directory(
            directory=agreement.dir,
            path=agreement.filename,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"{contact.siren}_bon_pour_accord.pdf",
        )
