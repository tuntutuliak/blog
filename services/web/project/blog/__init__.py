from flask import Blueprint

bp = Blueprint('blog', __name__)

from project.blog import routes 