from flask import Blueprint, render_template


top_app = Blueprint("top_app", __name__, static_folder='../static')


@top_app.route("/")
def top_info():
    return render_template("base.html")