from flask import Flask, request
from werkzeug.exceptions import BadRequest


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello my blog!"


@app.route("/user/")
def read_user():
    name = request.args.get("name")
    surname = request.args.get("surname")
    return f"User {name or '[no name]'} {surname or '[no surname]'}"


