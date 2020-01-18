import json
import flask

from flask import request
from flask_cors import CORS
from tinydb import TinyDB
from tinydb import Query

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


@app.route('/', methods=['GET'])
def home():
    return ''


@app.route('/api/v1/general', methods=['GET'])
def general():
    general = TinyDB('../db.json').table('general')
    data = general.all()[0]

    return json.dumps(data)


@app.route('/api/v1/validators', methods=['GET'])
def validators():
    onlyKnown = request.args.get('onlyKnown')

    validators = TinyDB('../db.json').table('validators')

    if onlyKnown is not None and onlyKnown.lower() == 'true':
        data = validators.search(Query().name != '')
    else:
        data = validators.all()

    return json.dumps(data)


if app.config["DEBUG"]:
    app.run(host='127.0.0.1', port=8000)
