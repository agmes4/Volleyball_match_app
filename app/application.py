from .models import match, team, tournament

def get_teams():
    return team.Team.query.all()