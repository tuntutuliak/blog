from flask import Flask, jsonify, send_from_directory, request, current_app
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.utils import secure_filename
from project.config import Config
from project.models import db
import os

migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'


def create_app(config_class=Config):
    app = Flask(__name__)  # Только один раз создаём приложение
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from project.models import User

    # Настройка папки для медиа-файлов
    app.config['MEDIA_FOLDER'] = os.path.join(app.root_path, 'services', 'web', 'media')

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from project.admin import init_admin
    with app.app_context():  # Добавляем контекст приложения
        init_admin(app)

    from project.main import bp as main_bp
    app.register_blueprint(main_bp)

    from project.blog import bp as blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')

    from project.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Маршрут для статических файлов
    @app.route("/static/<path:filename>")
    def staticfiles(filename):
        return send_from_directory(app.config["STATIC_FOLDER"], filename)

    # Маршрут для медиа-файлов
    @app.route("/media/<path:filename>")
    def mediafiles(filename):
        return send_from_directory(app.config["MEDIA_FOLDER"], filename)

    # Маршрут для загрузки файлов
    @app.route("/upload", methods=["GET", "POST"])
    def upload_file():
        if request.method == "POST":
            file = request.files["file"]
            filename = secure_filename(file.filename)
            # Сохраняем файл с уникальным именем
            file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
            return f'Файл {filename} загружен успешно!'

        return """
        <!doctype html>
        <title>Загрузить новый файл</title>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name=file><input type=submit value=Загрузить>
        </form>
        """

    return app
