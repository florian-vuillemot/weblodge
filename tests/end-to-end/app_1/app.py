"""
Basic application for deployment testing.
"""
import sys
from flask import Flask
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)


@app.route("/")
def hello_world():
    print('This is app 1 flush.', flush=True)
    print('This is app 1 err.', file=sys.stderr)
    logging.info('This is app 1 info.')
    logging.warning('This is app 1 warm.')
    logging.critical('This is app 1 critical.')
    return "This is app 1."
