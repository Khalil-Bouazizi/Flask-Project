import unittest

from app import app, db
from models import User


def create_app():
    app.config.from_object('project.config.TestingConfig')
    return app


class BaseTestCase(unittest):

    @classmethod
    def setUpClass(self):
        db.create_all()
        user = User(
            email="test@user.com",
            password="just_a_test_user",
            confirmed=False
        )
        db.session.add(user)
        db.session.commit()

    @classmethod
    def tearDownClass(self):
        db.session.remove()
        db.drop_all()