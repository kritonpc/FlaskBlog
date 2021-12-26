from app import db
from datetime import datetime, date
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=generate_uuid)
    gender = db.Column(db.Boolean, nullable=False)
    dob = db.Column(db.Date, nullable=True)
    username = db.Column(db.String(64), index=True, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))
    avatar = db.Column(db.String(256), default='avatar.png')
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    ip = db.Column(db.String(15))
    auth_token = db.Column(db.String(32), index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "gender": self.gender,
            "dob": self.dob,
            "username": self.username,
            "nickname": self.nickname,
            "description": self.description,
            "avatar": self.avatar,
            "email": self.email,
            "password_hash": self.password_hash,
            "ip": self.ip,
            "auth_token": self.auth_token
        }


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    desctiption = db.Column(db.String(256))
    image = db.Column(db.String(256))

    def __repr__(self):
        return '<Category {}>'.format(self.title)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "desctiption": self.desctiption,
            "image": self.image
        }


class Post(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(64))
    body = db.Column(db.String(256))
    poster_id = db.Column(db.String(64), db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    likes = db.relationship('Like', backref='post', lazy='dynamic')

    def __repr__(self):
        return '<Post {}>'.format(self.title)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "poster_id": self.poster_id,
        }

class Like(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=generate_uuid)
    post_id = db.Column(db.String(64), db.ForeignKey('post.id'))
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Like {}>'.format(self.id)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
        }

class Unlike(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=generate_uuid)
    post_id = db.Column(db.String(64), db.ForeignKey('post.id'))
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Unike {}>'.format(self.id)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
        }

class Comment(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=generate_uuid)
    post_id = db.Column(db.String(64), db.ForeignKey('post.id'))
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'))
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Comment {}>'.format(self.id)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "body": self.body,
            "timestamp": self.timestamp,
        }