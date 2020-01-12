import flask
import json
from flask import request, jsonify
from tinydb import TinyDB, Query


app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data in the form of a list of validators
'''validators = [
    {'id': 0,
     'name': 'fantom'},
    {'id': 1,
     'name': 'block42'}
]'''


@app.route('/', methods=['GET'])
def home():
    return '''<h1>API for Fantom Validator Infos - by block42</h1>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/fantom-validators/all', methods=['GET'])
def api_all():
    db = TinyDB('./../db/db.json')
    return json.dumps(db.all())
    #return jsonify(validators)

app.run()
