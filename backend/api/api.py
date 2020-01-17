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


@app.route('/api/v1/general', methods=['GET'])
def validators():
    return json.dumps(TinyDB('../db.json').table('general').all())


@app.route('/api/v1/validators', methods=['GET'])
def kpis():
    return json.dumps(TinyDB('../db.json').table('validators').all())


app.run(host='127.0.0.1', port=8000)
