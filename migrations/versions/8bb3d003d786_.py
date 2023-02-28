"""empty message

Revision ID: 8bb3d003d786
Revises: ff6c585686c8
Create Date: 2023-02-28 14:23:30.438230

"""
from alembic import op
import sqlalchemy as sa
from blog.app import db
from werkzeug.security import generate_password_hash


# revision identifiers, used by Alembic.
revision = '8bb3d003d786'
down_revision = 'ff6c585686c8'
branch_labels = None
depends_on = None


def upgrade():
    from blog.models import User
    admin = User(username="admin1", is_staff=True, email='admin1@mail.ru', password=generate_password_hash('space'))
    db.session.add(admin)
    db.session.commit()


def downgrade():
    pass
