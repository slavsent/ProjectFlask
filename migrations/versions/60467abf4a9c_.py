"""empty message

Revision ID: 60467abf4a9c
Revises: 26e847782dd1
Create Date: 2023-03-03 11:24:44.843639

"""
from alembic import op
import sqlalchemy as sa
from blog.app import db
from werkzeug.security import generate_password_hash

# revision identifiers, used by Alembic.
revision = '60467abf4a9c'
down_revision = '26e847782dd1'
branch_labels = None
depends_on = None


def upgrade():
    from blog.models import User
    admin = User(username="admin1", first_name='admin', is_staff=True, email='admin1@mail.ru',
                 password=generate_password_hash('space'))
    db.session.add(admin)
    db.session.commit()


def downgrade():
    pass
