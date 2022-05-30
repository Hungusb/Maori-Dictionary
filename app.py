from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error

# from pip._internal.network import session
# from pip._vendor.urllib3 import request

DB_NAME = "dictionary.db"
app = Flask(__name__)


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
        return False
    else:
        return True


@app.route('/')
def render_homepage():
    return render_template("home.html")


@app.route('/dictionary')
def render_dictionary():
    con = create_connection(DB_NAME)
    query = "SELECT Māori, English, Category, Definition, Level FROM words"
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    print(results)
    con.close()
    return render_template("dictionary.html", dictionary=results)


@app.route('/login', methods=["GET", "POST"])
def render_login():
    if is_logged_in():
        return redirect('/')
    print("in login")
    if request.method == "POST":
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()
        print(email)
        query = """SELECT id, fname, password FROM users WHERE email = ?"""
        con = create_connection(DB_NAME)
        cur = con.cursor()
        cur.execute(query, (email,))
        user_info = cur.fetchall()
        con.close()

    print(user_info)
        #compare user entered password to database password
        # if (password == user_info[0][2]):
        #     session['email'] = user_info[0][0]
        #     session['userid'] = user_info[0][1]
        #     session['firstname'] = user_info[0][0]
        # get data they entered
        # compare the data to what is in the database
        # login if they match
        # redirect if they do not.

        # try:
        #     user_id = user_info[0][0]
        #     first_name = [0][1]
        #     user_password = [0][2]
        # except:
        #     session['email'] = email
        #     session['userid'] = user_id
        #     session['firstname'] = first_name

    return render_template("login.html")

@app.route('/signup')

app.run(host='0.0.0.0', debug=True)
