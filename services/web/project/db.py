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
                Category(name='News', description='Latest cruise news and updates'),
                Category(name='Cruises', description='Information about different cruises'),
                Category(name='Traveling', description='Travel tips and guides'),
                Category(name='Tips', description='Useful tips for cruise travelers'),
                Category(name='Ships', description='Information about cruise ships')
            ]
            db.session.add_all(categories)
            
            # Создаем теги
            tags = [
                Tag(name='Cruises'),
                Tag(name='Tips'),
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
                    title='Why Choose Cruises Instead of Tours',
                    content='Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
                    image='images/sidebar-blog-1-370x264.jpg',
                    category_id=1,
                    author_id=1
                ),
                Post(
                    title='5 Adventure Cruises You Cannot Miss',
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