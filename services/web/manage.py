from flask.cli import FlaskGroup
from project import create_app, db
from project.models import User, Post, Category, Tag, Comment
from datetime import datetime
import os
import sys

cli = FlaskGroup(create_app=create_app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
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
    db.session.flush()  # Чтобы получить id пользователя
    
    # Создаем тестовые посты
    posts = [
        Post(
            title='Why Choose Cruises Instead of Tours',
            content='Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
            image='images/sidebar-blog-1-370x264.jpg',
            category_id=1,
            author_id=user.id
        ),
        Post(
            title='5 Adventure Cruises You Cannot Miss',
            content='Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua...',
            image='images/sidebar-blog-2-370x264.jpg',
            category_id=2,
            author_id=user.id
        )
    ]
    db.session.add_all(posts)
    
    # Сохраняем изменения
    db.session.commit()


@cli.command("load_mock_data")
def seed_mock_data():
    """Загружает тестовые данные из JSON файла"""
    # Добавляем путь к директории проекта в sys.path
    project_dir = os.path.dirname(os.path.abspath(__file__))
    if project_dir not in sys.path:
        sys.path.append(project_dir)
    
    from project.data.load_mock_data import load_mock_data
    load_mock_data()


if __name__ == "__main__":
    cli()
