from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    groups = db.relationship('Group', secondary='group_membership', back_populates='members')
    savings = db.relationship('Saving', backref='user', lazy=True)
    loans = db.relationship('Loan', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(256))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    members = db.relationship('User', secondary='group_membership', back_populates='groups')
    meetings = db.relationship('Meeting', backref='group', lazy=True)
    projects = db.relationship('Project', backref='group', lazy=True)

group_membership = db.Table('group_membership',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)

class Saving(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    date_saved = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    date_taken = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    interest_rate = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    paid = db.Column(db.Boolean, default=False)

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    date = db.Column(db.DateTime)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(512))
    state = db.Column(db.String(64))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(512))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)
