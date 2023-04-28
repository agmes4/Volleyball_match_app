
from . import db

tags_teams = db.Table('tags_team',
    db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True)
)

class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    teams = db.relationship('Team', secondary=tags_teams, lazy='subquery',
        backref=db.backref('teams', lazy=True))
    groups = db.Column(db.Integer, nullable=True)

    matches = db.relationship("Match", backref='post')

    def __init__(self, name: str, teams: list, groups=2):
        self.name = name
        self.teams = teams
        self.groups = groups

    def set_matches(self, matches: list):
        self.matches = matches

    def get_ongoing_matches(self) -> list:
        on = []
        for match in self.matches:
            if match.winner is None:
                on.append(match)
        return on
