from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, current_app, Markup
from flask_admin.form import ImageUploadField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from project.models import db, User, Post, Category, Tag, Comment
from flask_admin.form import ImageUploadField
from markupsafe import Markup

class ImageUploadWithPreviewField(ImageUploadField):
    def __call__(self, **kwargs):
        html = super().__call__(**kwargs)
        if self.data:
            image_url = f"/media/{self.data}"
            preview = Markup(f'<br><img src="{image_url}" style="max-height: 200px;">')
            return html + preview
        return html



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
    def __init__(self, model, session, media_folder, **kwargs):
        super().__init__(model, session, **kwargs)


    def scaffold_form(self):
        form_class = super().scaffold_form()
        form_class.image = ImageUploadWithPreviewField(
            'Изображение',
            base_path=current_app.config['MEDIA_FOLDER'],
            url_relative_path='media/'
        )
        return form_class


    column_list = ['id', 'title', 'user', 'category', 'created_at', 'updated_at']
    column_searchable_list = ['title', 'content']
    column_filters = ['category', 'user', 'created_at']
    form_columns = ['title', 'content', 'user', 'category', 'tags', 'image']

    form_overrides = {
        'tags': QuerySelectMultipleField,
        'image': ImageUploadField
    }

    form_args = {
        'user': {
            'query_factory': lambda: User.query.all(),
            'get_label': 'name'
        },
        'category': {
            'query_factory': lambda: Category.query.all(),
            'get_label': 'name'
        },
        'tags': {
            'query_factory': lambda: Tag.query.all(),
            'get_label': 'name'
        }
    }

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

    def _preview_image(view, context, model, name):
        if not model.image:
            return ''
        return Markup(f'<img src="/media/{model.image}" width="100">')

    column_formatters = {
        'image': _preview_image
    }


class CategoryAdmin(SecureModelView):
    column_list = ['name', 'description', 'posts_count']
    column_searchable_list = ['name', 'description']
    column_filters = ['name']
    form_columns = ['name', 'description']
    column_labels = {
        'name': 'Название',
        'description': 'Описание',
        'posts_count': 'Количество постов'
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
    media_folder = app.config['MEDIA_FOLDER']
    admin = Admin(app, name='Панель администратора', template_mode='bootstrap4')
    admin.add_view(UserAdmin(User, db.session,  name='Пользователи'))
    admin.add_view(PostAdmin(Post, db.session, media_folder=media_folder, name='Посты'))
    admin.add_view(CategoryAdmin(Category, db.session,  name='Категории'))
    admin.add_view(CommentAdmin(Comment, db.session, name='Комменты'))
    admin.add_view(SecureModelView(Tag, db.session, name='Теги'))