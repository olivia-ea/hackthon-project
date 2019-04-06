from flask import Flask, request, redirect, render_template, flash, session, jsonify, json, url_for
# from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
# import requests


app = Flask(__name__)
app.jinja_env.undefinded = StrictUndefined
app.debug = True

@app.route('/')
def index():
    """ Homepage """

    return render_template('homepage.html')