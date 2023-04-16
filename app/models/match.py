from sqlalchemy import Column

from . import db


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team1 = db.Column(db.Integer, db.ForeignKey('team.id'),
        nullable=False)
    team2 = db.Column(db.Integer, db.ForeignKey('team.id'),
                      nullable=False)
    point1 = db.Column(db.String(80), nullable=False)
    point2 = db.Column(db.String(80), nullable=False)
    point3 = db.Column(db.String(80), nullable=True)
    winner = db.Column(db.Integer, db.ForeignKey('team.id'),
        nullable=False)

    def __int__(self, team1: int, team2: int, points: list):
        self.team1 = team1
        self.team2 = team2
        if len(points) > 3:
            raise Exception("there are not more then 3 matches possible")
        wins_team1 = 0

        for count, point in enumerate(points, start=1):
            game_points = point.split(":")
            if game_points[0] > game_points[1]:
                wins_team1 += 1

            if count == 1:
                self.point1 = point
            if count == 2:
                self.point2 = point
            else:
                self.point3 = point

        if wins_team1 >= 2:
            self.winner = team1
        else:
            self.winner = team2

    def __repr__(self)-> str:
        output = f"Team: {self.team1} played against {self.team2}\n"
        output += f"with set 1 {self.point1}, set 2 {self.point2}, set 3 {self.point3}"
        return output


