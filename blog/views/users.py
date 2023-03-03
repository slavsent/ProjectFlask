from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.exceptions import NotFound
from blog.models import User
from flask_login import login_required, LoginManager, login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from blog.models.database import db
from blog.forms.user import UserRegisterForm, LoginForm
from werkzeug.security import generate_password_hash

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


@users_app.route("/register/", methods=["GET", "POST"], endpoint="register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users_app.details', user_id=current_user.id))

    errors = []
    form = UserRegisterForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count():
            form.username.errors.append("username already exists!")
            return render_template("users/register.html", form=form)

        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("email already exists!")
            return render_template("users/register.html", form=form)

        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            is_staff=False,
            user_img='',
            password=generate_password_hash(form.password.data)
        )

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create user!")
            errors.append = "Could not create user!"
        else:
            current_app.logger.info("Created user %s", user)
            login_user(user)
            return redirect(url_for('users_app.details', user_id=current_user.id))
    return render_template("users/register.html", form=form, errors=errors)
