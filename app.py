from datetime import datetime
import numpy as np
from flask import Flask, render_template, url_for, redirect, flash, session, request, send_file, abort
from flask_bcrypt import check_password_hash, Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_wtf import CSRFProtect
import pandas as pd
import codecs
import os
from os import environ
from models import db, User
from forms import RegisterForm, LoginForm, UploadFileForm
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from werkzeug.utils import secure_filename
from forms import LoginForm

bcrypt = Bcrypt()
csrf = CSRFProtect()
mail = Mail()


def send_registration_email(user_email):
    msg = Message("Welcome to Our Website!", sender='noreply@demo.com', recipients=[user_email])
    msg.body = "Thank you for registering with us!"
    mail.send(msg)


def create_app():
    app = Flask(__name__)
    app.config.from_json('config.json')
    db.init_app(app)
    migrate = Migrate(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    @app.route('/')
    def home():
        form = UploadFileForm()
        return render_template('index.html', form=form)

    @app.route('/back')
    def homeBack():
        if 'logged_in' in session and session['logged_in']:
            if session['role'] == 'ROLE_ADMIN':
                users = User.query.filter(User.role != 'ROLE_ADMIN').all()
                return render_template('back.html', users=users)
            else:
                session.pop('role', None)
                return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(
                firstname=form.firstName.data,
                lastname=form.lastName.data,
                email=form.email.data,
                phonenumber=form.telephone.data,
                password=hashed_password,
                confirmpassword=hashed_password,
                role="ROLE_USER",
                last_connection=datetime.utcnow()
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                flash('You have successfully registered', 'success')
                send_registration_email(new_user.email)

                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error: Registration failed. {str(e)}', 'error')

        return render_template('register.html', title='Register', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                flash('You have successfully logged in.', "success")
                session.clear()
                session['logged_in'] = True
                session['email'] = user.email
                session['lastname'] = user.lastname
                session['role'] = user.role

                if user.role == "ROLE_USER":
                    return redirect(url_for('home'))
                elif user.role == "ROLE_ADMIN":
                    return redirect(url_for('homeBack'))
            else:
                flash('Username or Password Incorrect', "danger")

        return render_template('login.html', form=form)

    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))

    @app.route('/delete/<int:mid>')
    def delete_user(mid):
        user = User.query.filter_by(id=mid).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully.', 'success')
        else:
            flash('User not found.', 'error')

        return redirect(url_for('homeBack'))

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        form = UploadFileForm()
        if form.validate_on_submit():
            file = form.file.data
            upload_folder = 'uploads'
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            file_path = os.path.join(upload_folder, secure_filename(file.filename))
            file.save(file_path)

            if file.filename.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file.filename.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                flash('Unsupported file type. Please upload a CSV or Excel file.', 'error')
                return redirect(url_for('upload_file'))

            df.drop_duplicates(inplace=True)
            df.dropna(axis=1, how='all', inplace=True)

            numeric_cols = df.select_dtypes(include=[np.number]).columns
            imputer = SimpleImputer(strategy='mean')
            df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

            df.fillna('', inplace=True)

            if not df[numeric_cols].empty:
                isolation_forest = IsolationForest(contamination=0.1)
                outliers = isolation_forest.fit_predict(df[numeric_cols])
                df = df[outliers != -1]

                scaler = StandardScaler()
                df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

            categorical_cols = df.select_dtypes(include=[object]).columns
            if not categorical_cols.empty:
                encoder = OneHotEncoder(sparse=False, drop='first')
                encoded_columns = encoder.fit_transform(df[categorical_cols])
                encoded_df = pd.DataFrame(encoded_columns, columns=encoder.get_feature_names_out(categorical_cols),
                                          index=df.index)

                print("Categorical columns:", categorical_cols)
                print("Encoded DataFrame shape:", encoded_df.shape)
                print("Original DataFrame shape before drop:", df.shape)

                df = df.drop(columns=categorical_cols)
                print("Original DataFrame shape after drop:", df.shape)

                df = pd.concat([df, encoded_df], axis=1)
                print("Final DataFrame shape after concat:", df.shape)

            sql_statements = generate_sql_statements(df)
            sql_file_path = 'cleaned_data.sql'

            with codecs.open(sql_file_path, 'w', encoding='utf-8') as sql_file:
                sql_file.write(sql_statements)

            os.remove(file_path)
            return send_file(sql_file_path, as_attachment=True)

        return render_template('index.html', form=form)

    def generate_sql_statements(df):
        table_name = 'test'
        sql_statements = ''
        for _, row in df.iterrows():
            columns = ', '.join(row.index)
            values = ', '.join([f"'{str(value)}'" for value in row.values])
            sql_statements += f"INSERT INTO {table_name} ({columns}) VALUES ({values});\n"
        return sql_statements

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
