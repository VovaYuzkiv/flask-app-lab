from app import db, loginManager
from flask_login import UserMixin
from datetime import datetime as dt

@loginManager.user_loader
def loadUser(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    imageFile = db.Column(db.String(40), nullable=True, default="default.png")
    aboutMe = db.Column(db.Text,nullable=True,default="")
    last_seen = db.Column(db.DateTime,nullable=True,default=dt.now())

    def __repr__(self):
        return f"User ('{self.username}')"