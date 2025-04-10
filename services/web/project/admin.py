from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from project.models import db, User, Category, Tag, Post, Comment

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))

class UserAdmin(SecureModelView):
    column_exclude_list = ['password']
    form_excluded_columns = ['password']

class PostAdmin(SecureModelView):
    column_list = ['title', 'category_id', 'author_id', 'created_at']
    column_searchable_list = ['title', 'content']
    column_filters = ['created_at', 'category_id', 'author_id']
    form_columns = ['title', 'content', 'image', 'category_id', 'author_id', 'tags']
    
    def _list_title(view, context, model, name):
        return model.title
    
    def _list_category(view, context, model, name):
        return model.category.name if model.category else ''
    
    def _list_author(view, context, model, name):
        return model.author.name if model.author else ''
    
    column_formatters = {
        'title': _list_title,
        'category_id': _list_category,
        'author_id': _list_author
    }
    
    form_widget_args = {
        'content': {'rows': 10, 'style': 'width: 100%'},
        'image': {'style': 'width: 100%'}
    }
    
    def get_form_choices(self):
        return {
            'category_id': [(c.id, c.name) for c in Category.query.all()],
            'author_id': [(u.id, u.name) for u in User.query.all()]
        }

def init_admin(app):
    admin = Admin(app, name='Админ-панель', template_mode='bootstrap4')
    
    admin.add_view(UserAdmin(User, db.session, name='Пользователи'))
    admin.add_view(SecureModelView(Category, db.session, name='Категории'))
    admin.add_view(SecureModelView(Tag, db.session, name='Теги'))
    admin.add_view(PostAdmin(Post, db.session, name='Посты'))
    admin.add_view(SecureModelView(Comment, db.session, name='Комментарии')) 