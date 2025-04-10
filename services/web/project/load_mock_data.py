import json
from datetime import datetime
from project import create_app, db
from project.models import User, Category, Tag, Post, Comment
from werkzeug.security import generate_password_hash

def load_mock_data():
    app = create_app()
    
    with app.app_context():
        # Очистка существующих данных
        Comment.query.delete()
        Post.query.delete()
        Tag.query.delete()
        Category.query.delete()
        User.query.delete()
        
        # Загрузка тестовых данных
        with open('project/data/mock_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Создание пользователей
        users = {}
        for user_data in data['users']:
            user = User(
                email=user_data['email'],
                password=generate_password_hash(user_data['password']),
                name=user_data['name'],
                role=user_data['role'],
                bio=user_data['bio'],
                avatar=user_data['avatar'],
                active=True
            )
            db.session.add(user)
            users[user.email] = user
        
        # Создание категорий
        categories = {}
        for category_data in data['categories']:
            category = Category(
                name=category_data['name'],
                description=category_data['description']
            )
            db.session.add(category)
            categories[category.name] = category
        
        # Создание тегов
        tags = {}
        for tag_data in data['tags']:
            tag = Tag(name=tag_data['name'])
            db.session.add(tag)
            tags[tag.name] = tag
        
        # Первый коммит для получения ID
        db.session.commit()
        
        # Создание постов
        posts = {}
        for post_data in data['posts']:
            post = Post(
                title=post_data['title'],
                content=post_data['content'],
                image=post_data['image'],
                category_id=categories[post_data['category']].id,
                author_id=users[post_data['author_email']].id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            # Добавление тегов к посту
            for tag_name in post_data['tags']:
                post.tags.append(tags[tag_name])
            
            db.session.add(post)
            posts[post.title] = post
        
        # Создание комментариев
        for comment_data in data['comments']:
            comment = Comment(
                post_id=posts[comment_data['post_title']].id,
                first_name=comment_data['first_name'],
                last_name=comment_data['last_name'],
                email=comment_data['email'],
                content=comment_data['content'],
                created_at=datetime.utcnow()
            )
            db.session.add(comment)
        
        # Финальный коммит
        db.session.commit()
        print("Тестовые данные успешно загружены!")

if __name__ == '__main__':
    load_mock_data() 