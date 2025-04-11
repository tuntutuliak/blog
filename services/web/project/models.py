from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
from slugify import slugify

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(80))
    role = db.Column(db.String(128), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(255))
    social_links = db.Column(db.JSON)
    posts = db.relationship('Post', backref='user', lazy=True)

    def __init__(self, email, name, password=None, role='user'):
        self.email = email
        self.name = name
        self.role = role
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password = password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, description=None):
        self.name = name
        self.description = description
        self.slug = slugify(name)

    def get_posts_count(self):
        return len(self.posts)

class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', secondary='post_tags', backref=db.backref('tags', lazy='dynamic'))

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy=True)
    category = db.relationship('Category', backref='posts', lazy=True)

    def __init__(self, title, content, category_id, author_id, image=None):
        self.title = title
        self.content = content
        self.category_id = category_id
        self.author_id = author_id
        self.image = image

    def get_image_url(self):
        if self.image:
            return f'/media/{self.image}'
        return None

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    approved = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, content, post_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.content = content
        self.post_id = post_id 