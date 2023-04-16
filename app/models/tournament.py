from . import db, team, match
from sqlalchemy import Column

tags_teams = db.Table('tags_team',
    db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True)
)
tags_matches = db.Table('tags_match',
    db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id'), primary_key=True),
    db.Column('match_id', db.Integer, db.ForeignKey('match.id'), primary_key=True)
)
class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teams = db.relationship('Team', secondary=tags_teams, lazy='subquery',
        backref=db.backref('teams', lazy=True))

    matches = db.relationship('Match', secondary=tags_matches, lazy='subquery',
        backref=db.backref('matches', lazy=True))