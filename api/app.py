import os

from flask import Flask


AGREEMENT_DIR = "/bpa"


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}".format(
    os.getenv("DB_USER", "root"),
    os.getenv("DB_PASSWORD", "root"),
    os.getenv("DB_HOST", "mysql"),
    os.getenv("DB_NAME", "db"),
)


from db import init_db
from urls import init_api
from mail import init_mail

init_api(app)
init_db(app)
init_mail(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
