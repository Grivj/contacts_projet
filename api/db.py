from faker import Faker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app: Flask):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        generate_fake_contacts()


def generate_fake_contacts(count: int = 100):
    """Generate fake contacts if number of contacts in the db is under $count"""
    from models.Contact import Contact

    if db.session.query(Contact).count() <= count:
        faker = Faker("fr_FR")
        fake_contacts = [
            Contact(
                name=faker.name(),
                phone_number="0643014673",
                email="jgriveau@yahoo.fr",
                # email=faker.email(),
                siren="838170918"
                # company=faker.company(),
            )
            for _ in range(10)
        ]
        db.session.add_all(fake_contacts)
        db.session.commit()
