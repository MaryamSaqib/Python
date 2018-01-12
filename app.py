import data
from flask import Flask, render_template, flash,redirect, url_for, session, logging
from flask_mysqldb import MySQL 
from wtforms import Form,StringField, TextAreaFiled, PasswordField, validators
from passlib.has import sha256_crypt

app = Flask(__name__)

app.debug=True

@app.route("/")
def index():
    return render_template("products_search.html", products = data.getProducts())

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('confirm password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():

        return render_template('register.hmtl', form=form) 
        
    



if __name__ == "__main__":
    app.run() 
