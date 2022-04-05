from db import db
from flask_restful import abort, fields
from sqlalchemy.inspection import inspect

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "company": fields.String,
    "siren": fields.String,
    "email": fields.String,
    "phone_number": fields.String,
    "called": fields.Boolean,
}


class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=True)
    name = db.Column(db.String(80), nullable=True)
    phone_number = db.Column(db.String(10), nullable=True)
    siren = db.Column(db.String(14), nullable=True)
    company = db.Column(db.String(80), nullable=True)
    called = db.Column(db.Boolean, default=False, nullable=True)

    def update(self, updated_contact: dict):
        for column in self.__table__.columns.keys():
            if column in updated_contact:
                setattr(self, column, updated_contact[column])

        db.session.commit()

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def get_contact_by_id_or_abort(id: int):
    contact = Contact.query.filter_by(id=id).first()
    if not contact:
        abort(404, message=f"Contact {id} doesn't exist")
    return contact


def if_empty_company_or_siren_abort(contact: Contact):
    if not contact.company or not contact.siren:
        abort(
            400, message=f"Contact with if: {id} has no company or siren number.")
