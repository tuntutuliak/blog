import json
import os
from datetime import datetime
from project import create_app, db
from project.models import User, Post, Category, Tag, Comment

def load_mock_data():
    # Получаем путь к файлу с данными
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(current_dir, 'mock_data.json')
    
    # Загружаем данные из JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    app = create_app()
    with app.app_context():
        # Очищаем базу данных
        db.drop_all()
        db.create_all()
        
        # Создаем пользователей
        users = {}
        for user_data in data['users']:
            user = User(
                email=user_data['email'],
                active=user_data['active'],
                name=user_data['name'],
                role=user_data['role'],
                bio=user_data['bio'],
                avatar=user_data['avatar'],
                facebook=user_data['facebook'],
                twitter=user_data['twitter'],
                instagram=user_data['instagram'],
                linkedin=user_data['linkedin']
            )
            db.session.add(user)
            users[user_data['email']] = user
        
        # Создаем категории
        categories = {}
        for cat_data in data['categories']:
            category = Category(
                name=cat_data['name'],
                description=cat_data['description']
            )
            db.session.add(category)
            categories[cat_data['name']] = category
        
        # Создаем теги
        tags = {}
        for tag_data in data['tags']:
            tag = Tag(name=tag_data['name'])
            db.session.add(tag)
            tags[tag_data['name']] = tag
        
        # Применяем изменения, чтобы получить ID
        db.session.flush()
        
        # Создаем посты
        posts = {}
        for post_data in data['posts']:
            post = Post(
                title=post_data['title'],
                content=post_data['content'],
                image=post_data['image'],
                category_id=categories[post_data['category']].id,
                author_id=users[post_data['author_email']].id
            )
            # Добавляем теги к посту
            for tag_name in post_data['tags']:
                post.tags.append(tags[tag_name])
            
            db.session.add(post)
            posts[post_data['title']] = post
        
        # Применяем изменения, чтобы получить ID постов
        db.session.flush()
        
        # Создаем комментарии
        for comment_data in data['comments']:
            comment = Comment(
                first_name=comment_data['first_name'],
                last_name=comment_data['last_name'],
                email=comment_data['email'],
                content=comment_data['content'],
                post_id=posts[comment_data['post_title']].id
            )
            comment.created_at = datetime.fromisoformat(comment_data['created_at'])
            db.session.add(comment)
        
        # Сохраняем все изменения
        db.session.commit()
        
        print("Mock data has been successfully loaded!")

if __name__ == '__main__':
    load_mock_data() 