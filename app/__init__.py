from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from .extensions import db

def create_app():
    app = Flask(__name__, template_folder="templates")

    app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///inventory.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
    db.init_app(app)
    from .routes.main import main_bp
    app.register_blueprint(main_bp)
    return app
