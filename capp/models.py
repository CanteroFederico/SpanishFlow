from capp import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database User
class User(db.Model, UserMixin):
    __tablename__ = "user_table"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    sentence = db.relationship('Sentence', backref='author', lazy=True)

# Database Sentence
class Sentence(db.Model):
    __bind_key__ = 'sentence'
    __tablename__= 'sentence_table'
    id = db.Column(db.Integer, primary_key=True)
    incorrect_sentence = db.Column(db.String)
    correct_sentence_one = db.Column(db.String)
    correct_sentence_two = db.Column(db.String)
    correct_sentence_three = db.Column(db.String)
    correct_sentence_four = db.Column(db.String)
    objective = db.Column(db.String)
    source = db.Column(db.String)
    your_sentence = db.Column(db.String)
    result_string = db.Column(db.String)
    result_num= db.Column(db.Float)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    group = db.Column(db.String)
    university = db.Column(db.String)
    year = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
