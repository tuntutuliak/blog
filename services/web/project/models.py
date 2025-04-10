from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    active = db.Column(db.Boolean(), default=True, nullable=False)
    name = db.Column(db.String(128))
    role = db.Column(db.String(128))
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(256))
    facebook = db.Column(db.String(256))
    twitter = db.Column(db.String(256))
    instagram = db.Column(db.String(256))
    linkedin = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, email, password, active=True, name=None, role=None, bio=None, avatar=None,
                 facebook=None, twitter=None, instagram=None, linkedin=None):
        self.email = email
        self.set_password(password)
        self.active = active
        self.name = name
        self.role = role
        self.bio = bio
        self.avatar = avatar
        self.facebook = facebook
        self.twitter = twitter
        self.instagram = instagram
        self.linkedin = linkedin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag', secondary=post_tags, lazy='joined',
                         backref=db.backref('posts', lazy=True))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __init__(self, title, content, category_id, author_id, image=None):
        self.title = title
        self.content = content
        self.category_id = category_id
        self.author_id = author_id
        self.image = image

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __init__(self, first_name, last_name, email, content, post_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.content = content
        self.post_id = post_id 