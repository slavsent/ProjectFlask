from flask_combo_jsonapi import ResourceDetail, ResourceList
from blog.schemas import ArticleSchema
from blog.models.database import db
from blog.models import Article
from combojsonapi.event.resource import EventsResource
from blog.api.permissions.article import ArticlePermission, ArticlePatchPermission


class ArticleListEvents(EventsResource):

    def event_get_count(self, **kwargs):
        return {"count": Article.query.count()}


class ArticleList(ResourceList):
    events = ArticleListEvents

    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
    }


class ArticleDetail(ResourceDetail):
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
        "permission_get": [ArticlePermission],
        "permission_patch": [ArticlePatchPermission],
    }
