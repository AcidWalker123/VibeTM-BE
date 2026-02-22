import os

from flask import Flask
from flask.cli import load_dotenv

from src.database.extensions import db
from src.web.controllers.user_controller import user_bp
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("POSTGRES_SQL_DB")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.register_blueprint(user_bp, url_prefix='/auth')

    db.init_app(app)

    return app

