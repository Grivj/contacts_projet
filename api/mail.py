import os

from flask import Flask
from flask_mail import Mail

mail = Mail()


def init_mail(app: Flask):
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
    app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True
    mail.init_app(app)
