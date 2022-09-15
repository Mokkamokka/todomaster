from todomaster import db
from datetime import datetime
from . import Todo


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    comment = db.Column(db.Text)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    todo_id = db.Column(db.Integer, db.ForeignKey(Todo.id), nullable=False)