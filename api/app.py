import os

from faker import Faker
from flask import Flask, Response, redirect, request, send_from_directory, url_for
from flask_restful import Api, Resource, abort
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from AgreementGenerator import AgreementGenerator

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

init_api(app)
init_db(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
