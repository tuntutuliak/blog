import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = os.path.join(basedir, "static")
    MEDIA_FOLDER = os.path.join(basedir, "media")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    UPLOAD_FOLDER = os.path.join(basedir, "media", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
