from .models import team, tournament
from . import db, Tournament, Match


def get_teams():
    return team.Team.query.all()


def generate_matches(tourn: int, level=1) -> list:
    tournament = Tournament.query.filter(id=tourn).first()
    if level == 1:
        teams = tournament.teams
    else:
        teams = []
    matches = []
    for team_index in range(0, int(len(teams) / tournament.groups), 2):
        match = Match(team1=teams[team_index].id, team2=teams[team_index + 1].id, tourn_id=tourn.id)
        db.session.add(match)
        db.session.commit()
        matches.append(match)
    return matches