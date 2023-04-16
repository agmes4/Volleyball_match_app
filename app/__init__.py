import os
from pathlib import Path

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

db = SQLAlchemy()
def creat_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True, instance_path=os.path.join(os.getcwd(), 'instance'))
    app.config["instance"] = os.path.join(os.getcwd(), 'instance')
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
        return "render_template()"

    return app