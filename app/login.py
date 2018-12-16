from flask import current_app
from flask_login import UserMixin


class UserLogin(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active


def get_login(username):
    db = current_app.config["db"]
    password = db.get_password(username)
    user = UserLogin(username, password) if password else None
    if user is not None:
        user.is_admin = user.username in current_app.config["ADMIN_USERS"]
    return user


