import data
from flask import Flask, render_template, flash,redirect, url_for, session, request, logging
from flask_mysqldb import MySQL 
from wtforms import Form,StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# config MYSQL 
app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = 'maryamsaqib2000' 
app.config['MYSQL_DB'] = 'myflaskapp' 
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# initialise MYSQL
mysql = MySQL(app)



app.debug=True

@app.route("/")
def index():
    return render_template("products_search.html")

class RegisterForm(Form):
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
        name = form.name.data 
        email = form.email.data 
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data)) 

        # create cursor
        cur = mysql.connection.cursor()

        # execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password)) 

        # commit to database 
        mysql.connection.commit()

        # close connection 
        cur.close() 

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('index'))

    return render_template('register.html', form=form) 

#user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        # Get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare passwords 
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('products'))
            else:
                error = 'Invalid password'
                return render_template('login.html', error = error)
            # Close connection 
            cur.close() 
        else:
            app.logger.info('NO USER')
    else:
        error = 'Username not found'
        return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please log in', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method=='POST':
        return render_template("products.html", productslist = data.getProducts(request.form['inputProduct'])) 
    else:
        return render_template("products.html")


if __name__ == "__main__":
    app.secret_key='secret123'
    app.run() 
