import json
import flask

from flask import request
from flask_cors import CORS

from tinydb import TinyDB
from tinydb import where

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return ""


@app.route("/api/v1/general", methods=["GET"])
def general():
    general = TinyDB("../db.json").table("general")
    data = general.all()[0]

    return json.dumps(data)


@app.route("/api/v1/validators", methods=["GET"])
def validators():
    hideUnknown = request.args.get("hideUnknown", default="false", type=str).lower()
    sortKey = request.args.get("sortKey", default=None, type=str)
    order = request.args.get("order", default="asc", type=str)

    validators = TinyDB("../db.json").table("validators")

    if hideUnknown == "true" or onlyKnown == "true":
        data = validators.search(where("name") != "")
    else:
        data = validators.all()

    if sortKey is not None:
        data = sorted(data, key=lambda validator: validator[sortKey], reverse=(order == "desc"))

    return json.dumps(data)


if app.config["DEBUG"]:
    app.run(host="127.0.0.1", port=8000)
