from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound
from blog.models import User
from flask_login import login_required

users_app = Blueprint("users_app", __name__, url_prefix='/users', static_folder='../static')


# USERS = {
#    1: "Ivan",
#    2: "Serge",
#    3: "Peter",
# }


@users_app.route("/", endpoint="list")
@login_required
def users_list():
    users = User.query.all()
    return render_template("users/list.html", users=users)


@users_app.route("/<int:user_id>/", endpoint="details")
@login_required
def user_details(user_id: int):
    # try:
    #    user_name = USERS[user_id]
    # except KeyError:
    #    raise NotFound(f"User #{user_id} doesn't exist!")
    # return render_template('users/details.html', user_id=user_id, user_name=user_name)
    user = User.query.filter_by(id=user_id).one_or_none()
    if user is None:
        raise NotFound(f"User #{user_id} doesn't exist!")
    return render_template("users/details.html", user=user)
