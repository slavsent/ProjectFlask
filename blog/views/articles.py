from flask import Blueprint, render_template
from blog.views.users import USERS
from werkzeug.exceptions import NotFound

articles_app = Blueprint("articles_app", __name__, url_prefix='/articles', static_folder='../static')

# ARTICLES = ["Flask", "Django", "JSON:API"]
ARTICLES = {
    1: {
        'title': 'Flask',
        'user': 2
    },
    2: {
        'title': 'Django',
        'user': 1
    },
    3: {
        'title': 'JSON:API',
        'user': 3
    },
}


@articles_app.route("/", endpoint="list")
def articles_list():
    return render_template("articles/list.html", articles=ARTICLES)


@articles_app.route("/<int:article_id>/", endpoint="details")
def user_details(article_id: int):
    try:
        article_name = ARTICLES[article_id]['title']
        article_user = USERS[(ARTICLES[article_id]['user'])]
    except KeyError:
        raise NotFound(f"Article #{article_id} doesn't exist!")
    return render_template('articles/details.html', article_id=article_id, article_name=article_name,
                           article_user=article_user)
