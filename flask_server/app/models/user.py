from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

from ..db import get_db

class User:

    def __init__(self, num, name, email, password_hash):
        self.num = num
        self.name = name
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def from_dict(user_dict):
        return User(
            user_dict["num"],
            user_dict["name"],
            user_dict["email"],
            user_dict["password_hash"],
        )

    def to_dict(self):
        return {
            "num" : self.num,
            "name" : self.name,
            "email" : self.email,
            "password_hash" : self.password_hash
        }

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except:
            return False

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"num" : self.num}).decode("utf-8")

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return None

        database = get_db()
        doc = database.collection(u"users").where(u"num", u"==", data["num"])
        return User.from_dict(doc.get().to_dict())