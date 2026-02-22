import datetime
import os
from datetime import timezone

import jwt
from flask.cli import load_dotenv

from src.core.user import User
from src.database.user_repository import UserRepository

load_dotenv()

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, username, password, email):
        user = User(username=username, email=email, password_hash=password)
        user.set_password(password)
        new_user = self.repository.save(user)
        return new_user

    def sign_in(self, username, password):
        user = self.repository.get(username)
        is_hash = user.check_password(password)
        if user is None:
            return False
        if is_hash:
            return self.generate_token(user.id)
        return is_hash

    def generate_token(self,user_id, expires_in=3600):
        """Generate a JWT token"""
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.now(timezone.utc) + datetime.timedelta(seconds=expires_in)
        }
        token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
        return token

    def verify_token(self, token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None