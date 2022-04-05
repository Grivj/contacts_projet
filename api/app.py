import os

from flask import Flask

from db import init_db
from mail import init_mail
from urls import init_api

AGREEMENT_DIR = "/bpa"


app = Flask(__name__)
for variable, value in os.environ.items():
    app.config[variable] = value


init_api(app)
init_db(app)
init_mail(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
