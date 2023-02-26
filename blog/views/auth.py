from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import logout_user, LoginManager, login_user, login_required
from werkzeug.security import check_password_hash
from blog.models import User

auth_app = Blueprint("auth_app", __name__, static_folder='../static')

login_manager = LoginManager()
login_manager.login_view = "auth_app.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_app.login"))


@auth_app.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Check your login details')
        return redirect(url_for(".login"))
    login_user(user)
    return redirect(url_for("users_app.details", user_id=user.id))


@auth_app.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))


@auth_app.route("/secret/")
@login_required
def secret_view():
    return "Super secret data"


__all__ = [
    "login_manager",
    "auth_app",
]
