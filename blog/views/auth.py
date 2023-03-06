from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import logout_user, LoginManager, login_user, login_required, current_user
from werkzeug.security import check_password_hash
from blog.models import User
from blog.forms.user import LoginForm


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
    if current_user.is_authenticated:
        return redirect(url_for('users_app.details', user_id=current_user.id))
    if request.method == 'GET':
        form = LoginForm(request.form)
        #return render_template('auth/login_old.html')
        return render_template('auth/login.html', form=form)

    errors = []
    form = LoginForm(request.form)
    email = form.email.data
    password = form.password.data
    #email = request.form.get('email')
    #password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        errors.append('Check your login details')
        return render_template("auth/login.html", form=form, errors=errors)
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
