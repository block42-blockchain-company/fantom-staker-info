import json

import flask
from tinydb import TinyDB

app = flask.Flask(__name__)
app.config["DEBUG"] = False


@app.route('/', methods=['GET'])
def home():
    return ''


@app.route('/api/v1/validators', methods=['GET'])
def validators():
    return json.dumps(TinyDB('../db.json').all())
