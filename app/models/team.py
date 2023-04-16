from sqlalchemy import Column
from app import db
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    matches = db.relationship('Team', lazy='select',
        backref=db.backref('match', lazy='joined'))

    def __int__(self, name: str):
        self.name = name

    def __repr__(self):
        return "Team: " + self.name