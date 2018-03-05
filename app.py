import data
from flask import Flask, render_template, flash,redirect, url_for, session, request, logging
from flask_mysqldb import MySQL 
from wtforms import Form,StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
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

# custom function to check if the logged in user has any existing suscriptions 
def isProductSubscribed(userid, productid):
    cur = mysql.connection.cursor()
    # Get user by username
    subscriptions = cur.execute("select * from subscriptions where userid = '%s' and productid ='%s'" % (userid, productid)) 

    if subscriptions > 0:
        return True
    else:
        return False

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

# Check if user logged in - we need this to prevent users from navigating to the page withpout being logged in
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
        #handle userid
        cur = mysql.connection.cursor() 
        result = cur.execute("select * from users where username = '%s'" % session['username']) # use the username from session and get the user id 
        result = cur.fetchone()
        if result > 0:
            userid = result['id']
        else:
            print 'No user'

        originalData = data.getProducts(request.form['inputProduct'])
        amendedData = []

        for sdata in originalData:
            isSubscribed = isProductSubscribed(userid, sdata['id']) 
            if isSubscribed:
                sdata['subscribed'] = 'Yes' #adding subscription staus to the data
            else:
                sdata['subscribed'] = 'No'
            
            amendedData.append(sdata) 
        return render_template("products.html", productslist = amendedData) 
    else:
        return render_template("products.html") 



@app.route('/subscribe', methods=['GET','POST']) 
@is_logged_in
def subscribe():
    if request.method == 'POST':
        productName = request.form['name']
        productPrice = request.form['price'][1:]
        productId = request.form['id']
        productImage = request.form['image']
        isProductSubscribed = request.form['subscribed']


        #Get id for user account
        cur = mysql.connection.cursor()

        # execute query
        cur.execute("select * from users where username = '%s'" % session['username']) 

        result = cur.fetchone()
        if result > 0:
            userId = result['id']
            if isProductSubscribed == 'No':
                #Add subscription
                cur.execute("insert into subscriptions (productid, productname, productprice, productimage, userid) values (%s, %s, %s, %s, %s)", (productId, productName, productPrice, productImage, userId))
                # commit to database 
                mysql.connection.commit()
            elif isProductSubscribed == 'Yes':
                #Remove subscription
                cur.execute("delete from subscriptions where userid = '%s' and productid = %s", (userId, productId))
                # commit to database 
                mysql.connection.commit()
        else:
            print 'Could not get user id'
    else:
        print 'Method is not a post'
        # close connection 
        cur.close() 
    #redo the search here to refresh data
    #maindata.getProducts(productSearch)
    return render_template('products.html') 


if __name__ == "__main__":
    app.secret_key='secret123'
    app.run() 

