from sqlalchemy import Column
from . import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __int__(self, name: str):
        self.name = name

    def __repr__(self):
        return "Team: " + self.name