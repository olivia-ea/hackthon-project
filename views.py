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
db_session = db_session()
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

    user = db_session.query(User).filter_by(user_id=username).first()

    if user:
        # flash("That username is already taken!")
        return redirect("/login-current-user")
    else:
        new_user = User(user_id=username, password=password)
        
        db_session.add(new_user)
        db_session.commit()

        user_id = new_user.user_id
        session['logged_user'] = {'username': username}

        # flash(f"User {username} added.")

        return redirect("/shopping-page")

@app.route('/login-current-user', methods=['GET'])
def login_form():

    return render_template("login-page.html")

@app.route('/login-verification', methods=["POST"])
def login_current_user():
    """ Login for Exisiting User """

    username = request.form.get("username")
    password = request.form.get("password")

    user = db_session.query(User).filter_by(user_id=username).first()

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

@app.route('/about')
def about():
    """ About """

    return render_template('about.html')

def generate_item(line):
    item = [x.strip() for x in line.split('|')]
    name = item[0]
    article_id = int(item[1])
    lot_number

@app.route("/shopping-page")
def display_package_clothing():
    """Display page for bulk clothing package."""


    # name, articleid, lot number, retailer, desciription, price, link

    item_list = []
    if db_session.query(Clothing).count() < 5:
        with open("clothing.txt") as f:
            for line in f:
                item = [x.strip() for x in line.split('|')]
                if len(item) < 7:
                    continue
                new_clothing = Clothing(
                        name=item[0],
                        article_id=int(item[1]),
                        lot_number=int(item[2]),
                        retailer=item[3],
                        description=item[4],
                        price=item[5],
                        link=item[6],
                        )
                db_session.add(new_clothing)
                db_session.commit()
    clothing = db_session.query(Clothing).all()
    print(clothing)
    return render_template("display_clothing.html", clothing=clothing)

@app.route("/cart")
def display_shopping_cart():
    """Display contents of shopping cart."""

    order_total = 0

    cart_clothing = []

    cart = session.get("cart", {})

    for clothing_id, quantity in cart.items():
        # Retrieve the clothing object corresponding to this id
        clothing = db_session.query(Clothing).filter_by(article_id = clothing_id).first()

        # Calculate the total cost for this type of clothing and add it to the
        # overall total for the order
        total_cost = quantity * clothing.price
        order_total += total_cost

        # Add the quantity and total cost as attributes on the Clothing object
        clothing.quantity = quantity
        clothing.total_cost = total_cost

        # Add the Clothing object to our list
        cart_clothing.append(clothing)

    # Pass the list of Clothing objects and the order total to our cart template
    return render_template("cart.html",
                           cart=cart_clothing,
                           order_total=order_total)

@app.route("/add_to_cart/<clothing_id>")
def add_to_cart(clothing_id):
    """Add a clothing item to cart and redirect to shopping cart page.

    When clothing is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message. """

    # Check if we have a cart in the session and if not, add one
    # Also, bind the cart to the name 'cart' for easy reference below
    if 'cart' in session:
        cart = session['cart']
    else:
        cart = session['cart'] = {}

    # Add clothing to cart - either increment the count (if clothing already in cart)
    # or add to cart with a count of 1
    cart[clothing_id] = cart.get(clothing_id, 0) + 1

    session['cart'] = cart
    # Show user success message on next page load
    flash("Item successfully added to cart.")

    # Redirect to shopping cart page
    return redirect("/cart")


@app.route("/checkout")
def checkout():
    """"Checkout customer, process payment, ect."""
    pass

@app.route('/logout')
def logout():
    """Log out."""

    session.clear()
    # flash("Logged Out.")

    return redirect("/")
