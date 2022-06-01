import sqlite3
from sqlite3 import Error

import flask_bcrypt
from flask import Flask, render_template, request, redirect, session

DB_NAME = "dictionary.db"
app = Flask(__name__)
app.secret_key = "breaker"


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        print("connection established")
        print(connection)
        return connection

    except Error as e:
        print(e)
    return


def is_logged_in():
    if session.get('email') is None:
        print("not logged in")
        return False
    print("logged in")
    return True

@app.route('/')
def render_homepage():
    return render_template("home.html", logged_in=is_logged_in())


@app.route('/dictionary')
def render_dictionary():
    con = create_connection(DB_NAME)
    query = "SELECT Māori, English, Category, Definition, Level FROM words"
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    print(results)
    con.close()
    return render_template("dictionary.html", dictionary=results, logged_in=is_logged_in())

@app.route('/logout')
def log_out():
    print(list(session.keys()))
    [session.pop(key) for key in list(session.keys())]
    print(list(session.keys()))
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def render_login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()

        con = create_connection(DB_NAME)
        query = """SELECT id, fname, password FROM users WHERE email = ?"""
        cur = con.cursor()
        cur.execute(query, (email,))
        user_info = cur.fetchall()
        con.close()

        try:
            user_id = user_info[0][0]
            first_name = user_info[0][1]
            db_password = user_info[0][2]
        except IndexError:
            return redirect("/login?error=Email+invalid+or+password+incorrect")

        if not flask_bcrypt.check_password_hash(db_password, password):
            return redirect(request.referrer + "?error=Email+invalid+or+password+incorrect")

        session['email'] = email
        session['user_id'] = user_id
        session['first_name'] = first_name
        print(session)
        return redirect('/')

    return render_template('/login.html', logged_in=is_logged_in())


@app.route('/signup', methods=['GET', 'POST'])
def render_signup():
    if request.method == 'POST':
        print(request.form)
        fname = request.form.get('fname').strip().lower()
        lname = request.form.get('lname').strip().lower()
        email = request.form.get('email').strip().lower()
        password = request.form.get('pass')
        password2 = request.form.get('pass2')

        if password != password2:
            return redirect('/signup?error=Passwords+do+not+match')

        if len(password) < 8:
            return redirect('/signup?error=Password+must+be+8+characters+or+more')

        hashed_password = flask_bcrypt.generate_password_hash(password)

        con = create_connection(DB_NAME)
        query = "INSERT INTO users(id, fname, lname, email, password) VALUES (NULL, ?, ?, ?, ?)"
        cur = con.cursor()

        try:
            cur.execute(query, (fname, lname, email, hashed_password))
        except sqlite3.IntegrityError:
            return redirect('/signup?error=email+is+already+in+use')
        con.commit()
        con.close()

    return render_template("signup.html")



app.run(host='0.0.0.0', debug=True)