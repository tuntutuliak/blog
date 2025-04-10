from flask_migrate import Migrate, init, migrate, upgrade
from project import create_app, db
from project.models import User, Category, Tag, Post, Comment

app = create_app()
migrate = Migrate(app, db)

@app.cli.command("create_db")
def create_db():
    """Создание базы данных"""
    with app.app_context():
        db.create_all()
        print("База данных создана!")

@app.cli.command("seed_db")
def seed_db():
    """Заполнение базы данных начальными данными"""
    with app.app_context():
        from project.load_mock_data import load_mock_data
        load_mock_data()
        print("База данных заполнена!")

if __name__ == '__main__':
    with app.app_context():
        print("Создание базы данных...")
        db.create_all()
        
        print("Загрузка тестовых данных...")
        from project.load_mock_data import load_mock_data
        load_mock_data()
        
        print("Инициализация завершена!")
