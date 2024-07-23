from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(80))
    firstname = db.Column(db.String(80))
    email = db.Column(db.String(120))
    phonenumber = db.Column(db.String(20))
    password = db.Column(db.String(200))
    confirmpassword = db.Column(db.String(200))
    role = db.Column(db.String(50))
    last_connection = db.Column(db.DateTime)
