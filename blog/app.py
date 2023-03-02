from flask import Flask, request, render_template
from werkzeug.exceptions import BadRequest
from flask_migrate import Migrate
from blog.views.users import users_app
from blog.views.articles import articles_app
from blog.views.top import top_app
from blog.models.database import db
from blog.views.auth import auth_app, login_manager


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object('blog.config')
    #app.config["SECRET_KEY"] = '7r3%huhsrm$p71_@cq(4bwhxfc90pf30e+s@tq!i40*psz^7k8'
    #app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)

    register_blueprints(app)

    login_manager.init_app(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(users_app)
    app.register_blueprint(articles_app)
    app.register_blueprint(top_app)
    app.register_blueprint(auth_app)
