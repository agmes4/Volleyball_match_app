
from . import db


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team1 = db.Column(db.Integer, db.ForeignKey('team.id'),
        nullable=False)
    team2 = db.Column(db.Integer, db.ForeignKey('team.id'),
                      nullable=False)
    point1 = db.Column(db.String(80), nullable=True)
    point2 = db.Column(db.String(80), nullable=True)
    point3 = db.Column(db.String(80), nullable=True)
    level = db.Column(db.Integer, nullable=False)
    winner = db.Column(db.Integer, db.ForeignKey('team.id'),
        nullable=True)
    tourn_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    def __init__(self, team1: int, team2: int, tourn_id: int, points=[], level=1):
        self.team1 = team1
        self.team2 = team2
        self.tourn_id = tourn_id
        self.level = level
        if len(points) > 3:
            raise Exception("there are not more then 3 matches possible")
        if len(points) > 0:
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

    def check_winner(self):
        if self.get_setindex() < 2:
            return
        wins_team1 = 0
        wins_team2 = 0

        for point in self.get_points():
            game_points = point.split(":")
            if game_points[0] > game_points[1]:
                wins_team1 += 1
            if game_points[1] > game_points[0]:
                wins_team2 += 1
        if wins_team1 >= 2:
            self.winner = self.team1
        elif wins_team2 >= 2:
            self.winner = self.team2
            db.session.commit()

    def __repr__(self) -> str:
        output = f"Team: {self.team1} played against {self.team2}\n"
        output += f"with set 1 {self.point1}, set 2 {self.point2}, set 3 {self.point3}"
        return output

    def set_points(self, points: str):
        set = self.get_setindex()
        if set == 3:
            raise Exception("Not a valid set")

        if set == 0:
            self.point1 = points
        else:
            if set == 1:
                self.point2 = points
            else:
                self.point3 = points
            self.check_winner()
        db.session.commit()

    def change_points(self, points, set):
        if set > self.get_setindex():
            raise Exception("the set you want to change wasnt added")
        if set == 0:
            self.point1 = points
        else:
            if set == 1:
                self.point2 = points
            else:
                self.point3 = points
        self.check_winner()
        db.session.commit()

    def get_setindex(self) -> int:
        if self.point3:
            return 3

        if self.point2:
            return 2

        if self.point1:
            return 1
        return 0

    def get_points(self) -> list:
        output_list = []
        match self.get_setindex():
            case 1:
                output_list.append(self.point1)
            case 2:
                output_list.append(self.point1)
                output_list.append(self.point2)
            case 3:
                output_list.append(self.point1)
                output_list.append(self.point2)
                output_list.append(self.point3)
        return output_list
