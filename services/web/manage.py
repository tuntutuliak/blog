from flask.cli import FlaskGroup
from project import create_app, db
from project.models import User, Category, Tag, Post, Comment
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)
cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    # Create admin user
    admin = User(
        email="admin@example.com",
        password="admin123",
        name="Admin",
        role="admin"
    )
    db.session.add(admin)

    # Create categories
    categories = [
        Category(name="Круизы", description="Статьи о круизах"),
        Category(name="Путешествия", description="Статьи о путешествиях"),
        Category(name="Советы", description="Полезные советы")
    ]
    for category in categories:
        db.session.add(category)

    # Create tags
    tags = [
        Tag(name="Морской круиз"),
        Tag(name="Карибы"),
        Tag(name="Средиземное море"),
        Tag(name="Советы путешественникам")
    ]
    for tag in tags:
        db.session.add(tag)

    db.session.commit()

if __name__ == "__main__":
    cli()
