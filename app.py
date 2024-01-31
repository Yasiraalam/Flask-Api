from flask import Flask
app = Flask(__name__)


@app.route("/")
def welcome():
    return "Home Page Yasir Alam"

@app.route("/home")
def home():
    return "Hi! welcome back to Home"

from controller import *