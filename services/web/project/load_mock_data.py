import json
import os
from datetime import datetime
from project import create_app, db
from project.models import User, Category, Tag, Post, Comment
from werkzeug.security import generate_password_hash
from sqlalchemy import inspect

def load_mock_data():
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Очистка существующих данных только если таблицы существуют
        if 'comments' in inspector.get_table_names():
            Comment.query.delete()
        if 'post_tags' in inspector.get_table_names():
            post_tags = db.Table('post_tags', db.metadata, extend_existing=True)
            db.session.execute(post_tags.delete())
        if 'posts' in inspector.get_table_names():
            Post.query.delete()
        if 'categories' in inspector.get_table_names():
            Category.query.delete()
        if 'tags' in inspector.get_table_names():
            Tag.query.delete()
        if 'users' in inspector.get_table_names():
            User.query.delete()
        db.session.commit()

        # Загрузка данных из JSON файла
        with open('project/data/mock_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Создание пользователей
        users = {}
        for user_data in data['users']:
            # Проверяем, существует ли пользователь
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user:
                users[user_data['email']] = existing_user
                continue
                
            user = User(
                email=user_data['email'],
                password=generate_password_hash(user_data['password']),
                name=user_data['name'],
                role=user_data['role'],
                active=True
            )
            db.session.add(user)
            users[user_data['email']] = user
        db.session.commit()

        # Создание категорий
        categories = {}
        for category_data in data['categories']:
            category = Category(
                name=category_data['name'],
                description=category_data['description']
            )
            db.session.add(category)
            categories[category_data['name']] = category
        db.session.commit()

        # Создание тегов
        tags = {}
        for tag_data in data['tags']:
            tag = Tag(name=tag_data['name'])
            db.session.add(tag)
            tags[tag_data['name']] = tag
        db.session.commit()

        # Создание постов
        for post_data in data['posts']:
            # Используем админа как автора по умолчанию
            author_email = post_data.get('author', 'admin@example.com')
            if author_email not in users:
                author_email = 'admin@example.com'  # Если указанный автор не существует, используем админа
                
            post = Post(
                title=post_data['title'],
                content=post_data['content'],
                image=post_data.get('image', ''),
                category_id=categories[post_data['category']].id,
                author_id=users[author_email].id
            )
            
            # Устанавливаем даты после создания объекта
            if 'created_at' in post_data:
                post.created_at = datetime.fromisoformat(post_data['created_at'])
            if 'updated_at' in post_data:
                post.updated_at = datetime.fromisoformat(post_data['updated_at'])
                
            db.session.add(post)
            
            # Добавление тегов к посту
            for tag_name in post_data.get('tags', []):
                if tag_name in tags:
                    post.tags.append(tags[tag_name])
            
            db.session.commit()

            # Создание комментариев для поста
            for comment_data in post_data.get('comments', []):
                # Используем текущую дату, если дата не указана
                comment_created_at = datetime.utcnow()
                if 'created_at' in comment_data:
                    comment_created_at = datetime.fromisoformat(comment_data['created_at'])
                    
                comment = Comment(
                    first_name=comment_data['first_name'],
                    last_name=comment_data['last_name'],
                    email=comment_data['email'],
                    content=comment_data['content'],
                    created_at=comment_created_at,
                    post_id=post.id
                )
                db.session.add(comment)
            
            db.session.commit()

        print("Тестовые данные успешно загружены!")

if __name__ == '__main__':
    load_mock_data() 