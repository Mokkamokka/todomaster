from todomaster import db
from . import UserModel


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey(UserModel.id), nullable=False)
