import logging
import os
import random
from pathlib import Path

from flask import Flask, render_template, request, flash, redirect, url_for, session

from .application import generate_matches
from .models import db
from .models.match import Match
from .models.team import Team
from .models.tournament import Tournament

log = logging.getLogger()

def creat_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True, instance_path=os.path.join(os.getcwd(), 'instance'))
    app.config["instance"] = os.path.join(os.getcwd(), 'instance')
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    if not os.path.exists(app.config.get("instance")):
        os.makedirs(app.config.get("instance"))
    if test_config:
        app.config = test_config
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(app.config["instance"], 'webserver.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if not os.path.exists(os.path.join(app.config["instance"], 'webserver.sqlite')):
        Path(os.path.join(app.config["instance"], 'webserver.sqlite')).touch()

    db.init_app(app)
    with app.app_context():
        from .models import team
        #db.drop_all()
        db.create_all()

    @app.route("/")
    def index():
        return render_template("home.html")

    @app.route("/teams")
    def teams():
        return render_template("teams.html", teams=team.Team.query.all())

    @app.route("/creat-team", methods=["POST"])
    def creat_team():
        name = request.form.get('team_name', None)
        if name is None:
            log.debug("the team name that was set is invalid")
            flash("team_error", "invalid name")
            return redirect(url_for('teams'))
        print(name)
        if Team.query.filter_by(name=name).first() is None:
            session.pop('_flashes', None)
            team = Team(name=name)
            db.session.add(team)
            db.session.commit()
        else:
            flash("team_error", "Team already exists ")
        return redirect(url_for('teams'))

    @app.route("/create-tournament", methods=["POST", "GET"])
    def create_touna():
        if request.method == "GET":
            return render_template("create_tournament.html", teams=Team.query.all())

        if len(request.form.getlist("team[]")) < 2 and \
                len(request.form.getlist("team[]")) % 2 == 0:
            flash("Tournament_error", "at least two teams mast be in an tournament")
            return render_template("create_tournament.html", teams=Team.query.all())
        teams = []
        for team in request.form.getlist("team[]"):
            teams.append(Team.query.filter_by(id=team).first())

        tourn = Tournament(name=request.form.get("tournament_name"), teams=teams, groups=request.form.get("groups", 2))
        random.shuffle(teams)

        db.session.add(tourn)
        db.session.commit()
        logging.debug(f"{request.form.get('groups', 2)=}")
        generate_matches(tourn.id)
        return redirect(f"/tournament?tourn={tourn.id}")

    @app.route("/tournament")
    def tourn():
        tourn_id = request.args.get("tourn", "")

        tourn = Tournament.query.filter_by(id=tourn_id).first()
        if tourn is None:
            return 404, "Tournament not found"

        return render_template("tournament.html", tourn=tourn)

    @app.route("/show-all-tournament")
    def all_tourns():
        return render_template("all_tourns.html", tourn=Tournament.query.all())

    @app.route("/newMatches/<tournamentid>", methods=["POST"])
    def generate_new_matches(tournamentid: int):
        generate_matches(tournamentid, 2)
        return redirect(f"/tournament?tourn={tournamentid}")

    @app.route("/addpoints/<matchid>", methods=["POST"])
    def add_points(matchid: int):
        match = Match.query.filter_by(id=matchid).first()
        match.set_points(f"{request.form.get('point_t1',0)}:{request.form.get('point_t2',0)}")
        db.session.commit()
        return redirect(f"/tournament?tourn={match.tourn_id}")

    return app
