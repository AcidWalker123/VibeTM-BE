import os
from src import create_app
from src.database.extensions import db
from src.core.user import User

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    env = os.getenv("FLASK_ENV")
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host='0.0.0.0' if env == "PROD" else '127.0.0.1',
        port=port,
        debug=False if env == "PROD" else True,
    )