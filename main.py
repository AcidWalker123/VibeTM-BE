from src import create_app
from src.database.extensions import db

from src.core.user import User

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

    app.run(debug=True)