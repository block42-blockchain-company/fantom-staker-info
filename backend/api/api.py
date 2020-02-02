import os
import json
import flask

from flask import request
from flask_cors import CORS

# Add project path to we can import the database
import sys
sys.path.append("../")

from modules.Database import Database


database = Database()

app = flask.Flask(__name__)
app.config["DEBUG"] = bool(os.environ["DEBUG"]) if "DEBUG" in os.environ.keys() else False
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return ""


@app.route("/api/v1/general", methods=["GET"])
def general():
    data = database.instance().general.find_one({}, {"_id": 0})
    return json.dumps(data)


@app.route("/api/v1/validators", methods=["GET"])
def validators():
    hideUnknown = request.args.get("hideUnknown", default="false", type=str).lower()
    sortKey = request.args.get("sortKey", default="_id", type=str)
    sortOrder = request.args.get("order", default="asc", type=str)

    data = database.getValidators(hideUnknown=hideUnknown, sortKey=sortKey, sortOrder=sortOrder)
    return json.dumps(data)


if app.config["DEBUG"]:
    app.run(host="127.0.0.1", port=8000)
