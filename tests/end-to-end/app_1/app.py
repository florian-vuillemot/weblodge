"""
Basic application for deployment testing.
"""
import sys
from flask import Flask
import logging

# Print INFO logs.
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route("/")
def hello_world():
    print('Log flush.', flush=True)
    print('Log on stderr.', file=sys.stderr)
    logging.info('Log info.')
    logging.warning('Log warm.')
    logging.critical('Log critical.')
    return "This is app 1."
