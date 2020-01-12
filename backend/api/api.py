import json

import flask
from flask_cors import CORS
from tinydb import TinyDB

app = flask.Flask(__name__)
app.config["DEBUG"] = False
CORS(app)


@app.route('/', methods=['GET'])
def home():
    return ''


@app.route('/api/v1/validators', methods=['GET'])
def validators():
    return json.dumps(TinyDB('../db.json').all())
