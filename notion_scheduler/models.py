from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notion_access_token = db.Column(db.String(255), nullable=False)
    notion_workspace_id = db.Column(db.String(255), nullable=False)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=True)
    date = db.Column(db.String(255), nullable=False)
