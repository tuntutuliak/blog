import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from project import db, create_app
from project.models import User, Post, Category, Tag, Comment
from datetime import datetime

def init_db():
    app = create_app()
    with app.app_context():
        # Создаем таблицы
        db.create_all()
        
        # Проверяем, есть ли уже данные
        if Category.query.first() is None:
            # Создаем категории
            categories = [
                Category(name='News', description='Последние новости и обновления'),
                Category(name='Tutorials', description='Информация о различных туториалах'),
                Category(name='Reviews', description='Обзоры и отзывы'),
                Category(name='Tips', description='Полезные советы для разработчиков'),
                Category(name='Tools', description='Информация об инструментах разработки')
            ]
            db.session.add_all(categories)
            
            # Создаем теги
            tags = [
                Tag(name='Cruises'),
                Tag(name='Tutorials'),
                Tag(name='Ships'),
                Tag(name='Recommendations'),
                Tag(name='Traveling'),
                Tag(name='News')
            ]
            db.session.add_all(tags)
            
            # Создаем тестового пользователя
            user = User(
                email='admin@example.com',
                active=True
            )
            db.session.add(user)
            
            # Создаем тестовые посты
            posts = [
                Post(
                    title='Почему выбирают наши туториалы',
                    content='Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
                    image='images/sidebar-blog-1-370x264.jpg',
                    category_id=1,
                    author_id=1
                ),
                Post(
                    title='5 обучающих туториалов, которые нельзя пропустить',
                    content='Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...',
                    image='images/sidebar-blog-2-370x264.jpg',
                    category_id=2,
                    author_id=1
                )
            ]
            db.session.add_all(posts)
            
            # Сохраняем изменения
            db.session.commit()

if __name__ == '__main__':
    init_db() 