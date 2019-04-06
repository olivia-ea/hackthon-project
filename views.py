from flask import Flask, request, redirect, render_template, flash, session, jsonify, json, url_for
# from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
# import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from model import User, Clothing


app = Flask(__name__)
app.jinja_env.undefinded = StrictUndefined
app.debug = True


##
# Import staticpool for the allowance of handling a connection over
# multiple threads, since Flask + SQlite gives an error when going from one page to another
# Initialize engine with connect_args: check_same_thread:False
# NOTE: http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html
from sqlalchemy.pool import StaticPool
engine = create_engine('sqlite:///clothingapp.db',\
        connect_args={'check_same_thread' : False}, poolclass=StaticPool)



# initializes a new database session connected to the
# sqlite3 engine. Using this object will allow you to
# add and query the database.
db_session = sessionmaker(bind=engine)
session = db_session()
# Example:
#       # Query Clothes
#       clothes = session.query(Clothing).all()
#       
#       # Add Clothes
#       newItem = Clothing(name="Pink Shirt", lot_number=15)
#       session.add(newItem)
#       session.commit()



@app.route('/')
def index():
    """ Homepage """
    return render_template('homepage.html')

@app.route('/register-new-user', methods=['GET'])
def register_new_user():

    return render_template('register-new-user.html')

@app.route('/sign-up-verification', methods=["POST"])
def register_process():
    """ Register New User """

    username = request.form["new-username"]
    password = request.form["new-password"]

    user = User.query.filter(User.user_id==username).first()

    if user:
        # flash("That username is already taken!")
        return redirect("/login-current-user")
    else:
        new_user = User(user_id=username, password=password)
        
        db.session.add(new_user)
        db.session.commit()

        user_id = new_user.user_id
        session['logged_user'] = {'username': username}

        # flash(f"User {username} added.")

        return redirect("/activity-page")

@app.route('/login-current-user', methods=['GET'])
def login_form():

    return render_template("login-page.html")

@app.route('/login-verification', methods=["POST"])
def login_current_user():
    """ Login for Exisiting User """

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter(User.user_id==username).first()

    if user:
        if user.password == password:
            user_id = user.user_id
            session['logged_user'] = {'username': user_id}
            # flash("You've successfully logged in!")
            return redirect("/shopping-page")
        else:
            return("The password is incorrect.")
    else:
        # flash("That username doesn't exist!")
        return redirect("/register-new-user")
