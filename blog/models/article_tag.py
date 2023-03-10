from sqlalchemy import Table, Column, Integer, ForeignKey
from blog.models.database import db

article_tag_association_table = Table(
    "article_tag_association",
    db.metadata,
    Column("article_id", Integer, ForeignKey("articles.id"), nullable=False),
    Column("tag_id", Integer, ForeignKey("tags.id"), nullable=False),
)
