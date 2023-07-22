"""
Basic application for deployment testing.
"""
from flask import Flask


myapp = Flask(__name__)


@myapp.route("/")
def hello_world():
    return "This is app 2."
