from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.sqlite3'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class ToDoList(db.Model):
    id = db.Column(db.Integer, primary_key = True)  
    task_name = db.Column(db.String(100))
    created_by = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, created_by):
        self.task_name = name
        self.created_by = created_by