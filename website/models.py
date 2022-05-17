from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class SavedJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10000))
    location = db.Column(db.String(10000))
    url = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    source = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    saved_jobs = db.relationship('SavedJob')

