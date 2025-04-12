import os
from datetime import timedelta

# Абсолютный путь до текущей папки (где лежит config.py)
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Подключение к БД (по умолчанию - PostgreSQL)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Статические файлы (CSS, JS, шрифты и т.д.)
    STATIC_FOLDER = os.path.join(basedir, "static")

    # Папка для медиа-файлов (загруженные пользователями картинки и т.п.)
    MEDIA_FOLDER = os.path.join(basedir, '..', 'media')  # services/web/media

    # Папка для upload-файлов, если отдельно используешь (может быть объединена с MEDIA_FOLDER)
    UPLOAD_FOLDER = os.path.join(
        os.environ.get('APP_FOLDER', '/usr/src/app'),
        'project/static/uploads'
    )

    # Безопасность
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Ограничение на размер загружаемого файла — 16MB
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # Разрешённые расширения для загрузки
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Настройки сессий
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Flask-Login remember-me cookie
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True

    # Темная/светлая тема для Flask-Admin
    FLASK_ADMIN_SWATCH = 'cerulean'
