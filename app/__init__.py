import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only")

    db.init_app(app)
    migrate.init_app(app, db)

    from app.paypal.client import PayPalClient
    app.extensions["paypal"] = PayPalClient()

    from app.routes.main import bp
    app.register_blueprint(bp)

    return app
