from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from project.models import db, User, Category, Tag, Post, Comment
from flask_admin.form import ImageUploadField
import os
from werkzeug.security import generate_password_hash

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))

class UserAdmin(SecureModelView):
    column_list = ['id', 'email', 'name', 'role', 'active', 'created_at']
    column_searchable_list = ['email', 'name']
    column_filters = ['role', 'active', 'created_at']
    form_columns = ['email', 'password', 'name', 'role', 'active', 'bio', 'avatar', 'social_links']
    column_labels = {
        'name': 'Имя',
        'email': 'Email',
        'role': 'Роль',
        'active': 'Активен',
        'created_at': 'Дата создания',
        'bio': 'Биография',
        'avatar': 'Аватар',
        'social_links': 'Социальные сети'
    }

class PostAdmin(SecureModelView):
    column_list = ['id', 'title', 'user', 'category', 'created_at', 'updated_at']
    column_searchable_list = ['title', 'content']
    column_filters = ['category', 'user', 'created_at']
    form_columns = ['title', 'content', 'user', 'category', 'tags', 'image']
    column_labels = {
        'title': 'Заголовок',
        'content': 'Содержание',
        'user': 'Автор',
        'category': 'Категория',
        'tags': 'Теги',
        'image': 'Изображение',
        'created_at': 'Дата создания',
        'updated_at': 'Дата обновления'
    }

class CategoryAdmin(SecureModelView):
    column_list = ['name', 'description', 'get_posts_count']
    column_searchable_list = ['name', 'description']
    column_filters = ['name']
    form_columns = ['name', 'description']
    column_labels = {
        'name': 'Название',
        'description': 'Описание',
        'get_posts_count': 'Количество постов'
    }

class CommentAdmin(SecureModelView):
    column_list = ['id', 'first_name', 'last_name', 'email', 'content', 'post', 'created_at']
    column_searchable_list = ['content', 'first_name', 'last_name', 'email']
    column_filters = ['post', 'created_at']
    form_columns = ['first_name', 'last_name', 'email', 'content', 'post']
    column_labels = {
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'email': 'Email',
        'content': 'Содержание',
        'post': 'Пост',
        'created_at': 'Дата создания'
    }

def init_admin(app):
    admin = Admin(app, name='Blog Admin', template_mode='bootstrap4')
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(PostAdmin(Post, db.session))
    admin.add_view(CategoryAdmin(Category, db.session))
    admin.add_view(CommentAdmin(Comment, db.session))