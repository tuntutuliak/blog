from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from project.models import db, User, Category, Tag, Post, Comment
from flask_admin.form import ImageUploadField
import os

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))

class UserAdmin(SecureModelView):
    column_exclude_list = ['password_hash']
    form_excluded_columns = ['password_hash']
    column_list = ['email', 'name', 'role', 'active', 'created_at']
    form_columns = ['email', 'name', 'role', 'active', 'bio', 'avatar', 'social_links']
    
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.set_password('password')

class PostAdmin(SecureModelView):
    column_list = ['title', 'category', 'user', 'created_at', 'image']
    column_searchable_list = ['title', 'content']
    column_filters = ['created_at', 'category', 'user']
    form_columns = ['title', 'content', 'image', 'category', 'user', 'tags']
    
    form_extra_fields = {
        'image': ImageUploadField('Image',
                                base_path=UPLOAD_FOLDER,
                                relative_path='posts/',
                                allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])
    }
    
    def _list_title(view, context, model, name):
        return model.title
    
    def _list_category(view, context, model, name):
        return model.category.name if model.category else ''
    
    def _list_author(view, context, model, name):
        return model.user.name if model.user else ''
    
    column_formatters = {
        'title': _list_title,
        'category': _list_category,
        'user': _list_author
    }
    
    form_widget_args = {
        'content': {'rows': 20, 'style': 'width: 100%'},
        'image': {'style': 'width: 100%'}
    }
    
    def get_form_choices(self):
        return {
            'category': [(c.id, c.name) for c in Category.query.all()],
            'user': [(u.id, u.name) for u in User.query.all()]
        }

class CommentAdmin(SecureModelView):
    column_list = ['post', 'first_name', 'last_name', 'email', 'created_at']
    column_searchable_list = ['content', 'email']
    column_filters = ['created_at', 'post']
    form_columns = ['post', 'first_name', 'last_name', 'email', 'content']

def init_admin(app):
    admin = Admin(app, name='Админ-панель', template_mode='bootstrap4')
    
    admin.add_view(UserAdmin(User, db.session, name='Пользователи'))
    admin.add_view(SecureModelView(Category, db.session, name='Категории'))
    admin.add_view(SecureModelView(Tag, db.session, name='Теги'))
    admin.add_view(PostAdmin(Post, db.session, name='Посты'))
    admin.add_view(CommentAdmin(Comment, db.session, name='Комментарии')) 