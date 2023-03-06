from sqlalchemy import Column, Integer, String, Boolean
from blog.models.database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(120), unique=False, nullable=False, default="", server_default="")
    last_name = Column(String(120), unique=False, nullable=False, default="", server_default="")
    username = Column(String(80), unique=True, nullable=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    email = Column(String(255), unique=True)
    password = Column(String(255), unique=True)
    user_img = Column(String(255))

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"

    def __init__(self, email, first_name, last_name, password, username, is_staff, user_img):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.username = username
        self.is_staff = is_staff
        self.user_img = user_img
