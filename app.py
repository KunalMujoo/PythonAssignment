from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
 
app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'

 
DB_HOST = "localhost"
DB_NAME = "pythonassignment"
DB_USER = "postgres"
DB_PASS = "1234"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
 
@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        if session['username'] == 'admin':
            return render_template('adminhome.html', username=session['username'])
        else:
            return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
 
@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(password)
 
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
 
        if account:
            hashed_pwd = account['password']
            
            # If account exists in users table in out database
            
            if check_password_hash(hashed_pwd, password):
            # if password == password_rs:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')
 
    return render_template('login.html')
  
@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
 
        #Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        print(account)
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        else:
        # Account doesnt exists and the form data is valid, now insert new account into users table
            # salt = bcrypt.gensalt()
            # password = password.encode('utf-8')
            # hashed_pwd = bcrypt.hashpw(password,salt)
            hashed_pwd = generate_password_hash(password)
            cursor.execute("INSERT INTO users (fullname, username, password, email) VALUES (%s,%s,%s,%s)", (fullname, username,hashed_pwd, email))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')


@app.route('/addbooks', methods=['POST'])
def addbooks():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'bookname' in request.form and 'authorname' in request.form and 'numberofcopies' in request.form:
        print('Hello world')
        bookname = request.form['bookname']
        authorname = request.form['authorname']
        numberofcopies = request.form['numberofcopies']
    
        cursor.execute('SELECT * FROM books WHERE bookname = %s', (bookname,))
        book = cursor.fetchone()
        print(book)
        # If account exists show error and validation checks
        if book:
            #add nummber of copies in the database
            flash('Book already exists')
            return 'Book exists'
        else:
            cursor.execute("INSERT INTO books (bookname, authorname, numberofcopies) VALUES (%s,%s,%s)", (bookname, authorname, numberofcopies))
            conn.commit()
            flash('Books added')
            return 'Books Added'
            

@app.route('/deletebooks', methods=['DELETE'])
def deletebooks():
    
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'DELETE' and 'bookname' in request.form:
        bookname = request.form['bookname']
        print(bookname)
        cursor.execute('DELETE FROM books WHERE bookname = %s', (bookname,))
        conn.commit()
        return 'Deleted Successfully'

@app.route('/viewbooks', methods=['GET'])
def viewbooks():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'GET':
        
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        return {
            "bookname": books[0][1],
            "authorname":books[0][2],
            "numberofcopies":books[0][3]
        }

@app.route('/borrowbook', methods=['POST'])
def borrowbook():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #the book name is given, so assign it to that user

    if request.method == 'POST' and 'bookname'in request.form:
        bookname = request.form['bookname']
        print(bookname)
        cursor.execute('INSERT into borrow (userid,bookid) VALUES (%s,%s)',(userid,bookid))
        conn.commit()

@app.route('/returnbook', methods=['POST'])
def returnbook():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'bookname'in request.form:
        bookname = request.form['bookname']
        print(bookname)
        cursor.execute('DELETE from borrow where bookname =  (%s)',(bookid,))
        conn.commit()


if __name__ == "__main__":
    app.run(debug=True)