import os
from flask import Flask, jsonify, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.utils import secure_filename

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'

def create_app():
    app = Flask(__name__)
    app.config.from_object("project.config.Config")
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    from project.models import User
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    from project.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from project.blog import bp as blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')
    
    from project.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.route("/static/<path:filename>")
    def staticfiles(filename):
        return send_from_directory(app.config["STATIC_FOLDER"], filename)

    @app.route("/media/<path:filename>")
    def mediafiles(filename):
        return send_from_directory(app.config["MEDIA_FOLDER"], filename)

    @app.route("/upload", methods=["GET", "POST"])
    def upload_file():
        if request.method == "POST":
            file = request.files["file"]
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
        return """
        <!doctype html>
        <title>upload new File</title>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name=file><input type=submit value=Upload>
        </form>
        """
    
    return app
