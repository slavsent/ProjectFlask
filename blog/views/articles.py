import requests
from flask import Blueprint, render_template, request, current_app, redirect, url_for
# from blog.views.users import USERS
from typing import Dict
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from blog.models.database import db
from blog.models import Author, Article, Tag
from blog.forms.article import CreateArticleForm

articles_app = Blueprint("articles_app", __name__, url_prefix='/articles', static_folder='../static')


# ARTICLES = ["Flask", "Django", "JSON:API"]
# ARTICLES = {
#    1: {
#        'title': 'Flask',
#        'user': 2
#    },
#    2: {
#        'title': 'Django',
#        'user': 1
#    },
#    3: {
#        'title': 'JSON:API',
#        'user': 3
#    },
# }


@articles_app.route("/", endpoint="list")
def articles_list():
    articles = Article.query.all()
    # call RPC method
    count_articles: Dict = requests.get('http://127.0.0.1:5000/api/articles/event_get_count/').json()
    return render_template("articles/list.html", articles=articles, count_articles=count_articles['count'])


@articles_app.route("/<int:article_id>/", endpoint="details")
def article_details(article_id):
    article = Article.query.filter_by(id=article_id).options(joinedload(Article.tags)).one_or_none()

    if article is None:
        raise NotFound
    return render_template("articles/details.html", article=article)


@articles_app.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = []
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    if request.method == "POST" and form.validate_on_submit():
        article = Article(title=form.title.data.strip(), body=form.body.data)
        db.session.add(article)
        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                article.tags.append(tag)
        if current_user.author:
            # use existing author if present
            article.author_id = current_user.author.id
        else:
            # otherwise create author record
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            article.author_id = author.id
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")
            error.append("Could not create article!")
        else:
            return redirect(url_for("articles_app.details", article_id=article.id))

    return render_template("articles/create.html", form=form, error=error)
