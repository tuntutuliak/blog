from flask.cli import FlaskGroup
from project import create_app, db

cli = FlaskGroup(create_app())


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    from project.models import User
    db.session.add(User(email="michael@mherman.org"))
    db.session.commit()


if __name__ == "__main__":
    cli()
