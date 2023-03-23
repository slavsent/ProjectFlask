from combojsonapi.permission.permission_system import (
    PermissionMixin,
    PermissionUser,
    PermissionForGet,
    PermissionForPatch,
)
from flask_combo_jsonapi.exceptions import AccessDenied
from flask_login import current_user
from blog.models import User, Article, Author


class ArticlePermission(PermissionMixin):

    def get(self, *args, many=True, user_permission: PermissionUser = None, **kwargs) -> PermissionForGet:

        if not current_user.is_authenticated:
            raise AccessDenied("no access")
        author_id = Author.query.filter_by(user_id=current_user.id).one_or_none()
        if not author_id:
            raise AccessDenied("no access")
        if not current_user.is_staff:
            self.permission_for_get.filters.append(Article.author_id == current_user.author.id)
        return self.permission_for_get


class ArticlePatchPermission(PermissionMixin):

    def patch_permission(self, *args, user_permission: PermissionUser = None, **kwargs) -> PermissionForPatch:
        if not current_user.is_authenticated:
            raise AccessDenied("no access")
        author_id = Author.query.filter_by(user_id=current_user.id).one_or_none()
        if not author_id:
            raise AccessDenied("no access")
        return self.permission_for_patch

    def patch_data(self, *args, data: dict = None, obj: User = None, user_permission: PermissionUser = None,
                   **kwargs) -> dict:
        id_article = int(data.get('id'))
        author_id = Author.query.filter_by(user_id=current_user.id).one_or_none()
        if author_id:
            article = Article.query.filter_by(id=id_article, author_id=current_user.author.id)
            if not article:
                if not current_user.is_staff:
                    raise AccessDenied("no access")
            return data
        else:
            raise AccessDenied("no access")
