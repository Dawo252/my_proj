# models.py

from flask_login import UserMixin
from . import db
from sqlalchemy import delete
from sqlalchemy.orm import backref


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    bio = db.Column(db.Text)
    photo = db.Column(db.String(500))
    threads = db.relationship('ForumThread', backref='user_thread')
    posts = db.relationship('ForumPost', backref='user_post')

    def __repr__(self):
        return f'<User {self.username}>'


class ForumThread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posts = db.relationship('ForumPost', backref='forum_thread')
    subject = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<thread: {self.id, self.user_id, self.posts, self.subject}>'


class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('forum_thread.id'))
    contents = db.Column(db.String(5000), unique=False, nullable=False)

    def __repr__(self):
        return f'<post: {self.id, self.thread_id, self.contents}>'
