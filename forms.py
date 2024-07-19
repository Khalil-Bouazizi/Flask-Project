from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField, HiddenField, FileField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length, Regexp, InputRequired

from models import User


def validate_email(form, field):
    user = User.query.filter_by(email=field.data).first()
    if user is not None:
        raise ValidationError('Email already registered.')


def validate_phoneNumber(form, field):
    user = User.query.filter_by(phonenumber=field.data).first()
    if user is not None:
        raise ValidationError('Phone Number already registered.')


class RegisterForm(FlaskForm):
    firstName = StringField('First Name', validators=[
        InputRequired(message="First Name is required."),
        Length(min=2, max=20, message="First Name must be between 2 and 20 characters.")
    ])
    lastName = StringField('Last Name', validators=[
        InputRequired(message="Last Name is required."),
        Length(min=2, max=20, message="Last Name must be between 2 and 20 characters.")
    ])
    telephone = StringField('Telephone', validators=[
        InputRequired(message="Telephone number is required."),
        Length(min=8, max=8, message="Telephone number must be exactly 8 digits."),
        Regexp(r'^[0-9]*$', message="Telephone must contain only digits."),
        validate_phoneNumber
    ])
    email = StringField('Email', validators=[
        InputRequired(message="Email is required."),
        Email(message="Invalid email address."),
        validate_email
    ])
    password = PasswordField('Password', validators=[
        InputRequired(message="Password is required."),
        Length(min=8, message="Password must be at least 8 characters long."),
        Regexp(
            regex=r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',
            message="Password must contain at least one letter, one number, and one special character."
        )
    ])
    confirmPassword = PasswordField('Confirm Password', validators=[
        InputRequired(message="Please confirm your password."),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        InputRequired(message="Email is required."),
        Email(message="Invalid email address.")
    ])
    password = PasswordField('Password', validators=[
        InputRequired(message="Password is required.")
    ])
    submit = SubmitField('Login')


class DeleteForm(FlaskForm):
    delete_id = HiddenField("Hidden table row ID")
    delete = SubmitField("Delete")


class UploadFileForm(FlaskForm):
    file = FileField('Upload CSV or Excel File', validators=[DataRequired()])
    submit = SubmitField('Upload')
