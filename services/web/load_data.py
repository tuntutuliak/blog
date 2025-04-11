from project import create_app, db
from project.load_mock_data import load_mock_data

app = create_app()
with app.app_context():
    load_mock_data() 