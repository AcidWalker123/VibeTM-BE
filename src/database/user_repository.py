from src.core.user import User
from src.database.extensions import db

class UserRepository:
    def __init__(self):
        self.db = db.session()

    def get(self, username):
        user = self.db.query(User).filter_by(username=username).first()
        return user

    def save(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, username, email, password):
        user = self.get(username)
        user.username = username
        user.email = email
        user.password = password
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, username):
        user = self.get(username)
        self.db.delete(user)
        self.db.commit()
        self.db.refresh(user)
        return user