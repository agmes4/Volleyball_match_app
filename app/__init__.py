import os
from pathlib import Path

from flask import Flask, render_template, request, flash, redirect, url_for, session
from .models import db, team, match, tournament
from .application import get_teams
from sqlalchemy.sql import func

from .models.team import Team


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
        from .models import match, team, tournament
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
            flash("team_error", "invalid name")
            return redirect(url_for('teams'))
        print(name)
        if Team.query.filter_by(name=name).first() is None:
            session.pop('_flashes', None)
            team = Team(name=name)
            db.session.add(team)
            db.session.commit()
        flash("team_error", "Team already exists ")
        return redirect(url_for('teams'))

    return app