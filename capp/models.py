from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import JSON
from capp import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Category Model
class Category(db.Model):
    __tablename__ = "category_table"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    sections = db.relationship('Section', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"

# Section Model
class Section(db.Model):
    __tablename__ = "section_table"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category_table.id'), index=True, nullable=False)
    icon = db.Column(db.String(100), nullable=True)

    sentences = db.relationship('Sentence', back_populates='section', lazy=True)

    def __repr__(self):
        return f"<Section {self.name}, Category ID: {self.category_id}>"

# Sentence Model
class Sentence(db.Model):
    __tablename__ = 'sentence_table'
    id = db.Column(db.Integer, primary_key=True)
    english_sentence = db.Column(db.String(500), nullable=False)
    spanish_sentence = db.Column(db.String(500), nullable=False)
    explanation_english = db.Column(db.String(500), nullable=False)
    explanation_spanish = db.Column(db.String(500), nullable=False)
    image_path = db.Column(db.String(100), nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category_table.id'), nullable=False)
    category = db.relationship('Category', backref='sentences', lazy=True)

    section_id = db.Column(db.Integer, db.ForeignKey('section_table.id'), index=True, nullable=False)
    section = db.relationship('Section', back_populates='sentences', lazy=True)

    def __repr__(self):
        return f"<Sentence {self.english_sentence[:50]}...>"

# User Model
class User(db.Model, UserMixin):
    __tablename__ = "user_table"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    progress = db.Column(JSON, nullable=True, default=dict)

    def __repr__(self):
        return f"<User {self.username}>"

# UserProgress Model
class UserProgress(db.Model):
    __tablename__ = 'user_progress_table'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), index=True, nullable=False)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentence_table.id', ondelete='CASCADE'), index=True, nullable=False)
    learned = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship('User', backref='user_progress', lazy=True)
    sentence = db.relationship('Sentence', backref=db.backref('sentence_progress', cascade='all, delete-orphan'), lazy=True)

    def __repr__(self):
        return f"<UserProgress User ID: {self.user_id}, Sentence ID: {self.sentence_id}>"
