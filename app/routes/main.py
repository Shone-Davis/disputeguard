import requests
from flask import Blueprint, current_app, render_template
from sqlalchemy import text

from app import db
from app.paypal.client import PayPalError

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    try:
        db.session.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    disputes, error = [], None
    try:
        disputes = current_app.extensions["paypal"].list_disputes()
    except (PayPalError, requests.RequestException) as e:
        error = str(e)

    return render_template("index.html", disputes=disputes, error=error, db_ok=db_ok)
