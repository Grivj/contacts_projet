from flask import Flask
from flask_restful import Api

from views.Agreement import DownloadAgreement, GenerateAgreement
from views.Contact import ContactInfo, ContactList
from views.Scrapper import ScrapperCompanyName
from views.Tunnel import Tunnel

# from views.Mailing import Mailing


def init_api(app: Flask):
    api = Api(app)
    api.add_resource(ContactList, "/contacts")
    api.add_resource(ContactInfo, "/contacts/<int:id>")
    api.add_resource(Tunnel, "/tunnel")
    api.add_resource(ScrapperCompanyName, "/scrapper_company_name/<string:siren>")
    api.add_resource(GenerateAgreement, "/contacts/<int:id>/generate_agreement")
    api.add_resource(DownloadAgreement, "/contacts/<int:id>/download_agreement")
    # api.add_resource(Mailing, "/contacts/<int:id>/mailing")
