import datetime

from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, index=True, default=datetime.datetime.now())
    start_time = db.Column(db.DateTime, index=True, nullable=True)
    exec_time = db.Column(db.DateTime, index=True, nullable=True)

    def __repr__(self):
        return '<Task {}>'.format(self.id)
