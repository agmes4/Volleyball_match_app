
from .models import team, db
from .models.match import Match
from .models.tournament import Tournament



def get_teams():
    return team.Team.query.all()


def get_teams_level(tourn, level=0) -> dict:
    if level == 0:
        return {1: tourn.teams}
    # TODO: Add the capability for more then tow levels
    elif level == 1:
        matches = Match.query.filter_by(id=tourn.id).all()
        output = {1: [], 2: []}
        for match in matches:
            output[1].append(match.winner)
            if match.team1 != match.winner:
                output[2].append(match.team1)
            else:
                output[2].append(match.team2)
    else:
        generate_matches(tourn, level - 1)
    return output


def generate_matches(tourn: int, level=1) -> list:
    tournament = Tournament.query.filter_by(id=tourn).first()
    matches = []
    dic = get_teams_level(tournament, level=level - 1)

    for level in dic:
        teams = dic[level]
        for team_index in range(0, int(len(teams) / tournament.groups), 2):
            match = Match(team1=teams[team_index].id, team2=teams[team_index + 1].id, tourn_id=tourn, level=level)
            db.session.add(match)
            db.session.commit()
            matches.append(match)
    tournament.set_matches(matches)
    db.session.commit()
    return matches
