"""
Basic application for deployment testing.
"""
import os
from flask import Flask


myapp = Flask(__name__)


@myapp.route("/")
def hello_world():
    return os.environ.get('RESULT', "This is app 2.")
