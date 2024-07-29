from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    phonenumber = db.Column(db.String(20))
    password = db.Column(db.String(200))
    confirmpassword = db.Column(db.String(200))
    role = db.Column(db.String(50))
    last_connection = db.Column(db.DateTime)
