from datetime import datetime

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(1200), unique=True, nullable=False)
    phonenumber = db.Column(db.String(1000), unique=True, nullable=False)
    password = db.Column(db.String(15000), nullable=False)
    confirmpassword = db.Column(db.String(15000), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    last_connection = db.Column(db.DateTime, default=datetime.utcnow)


def __repr__(self):
    return f'<User {self.firstname} {self.lastname}>'
