from app import create_app, db
import pytest
import os

os.environ["DATABASE_URL"] = "postgresql+psycopg://localhost/disputeguard_test"
os.environ["PAYPAL_CLIENT_ID"] = "test-id"
os.environ["PAYPAL_CLIENT_SECRET"] = "test-secret"
os.environ["PAYPAL_BASE_URL"] = "https://api.test.paypal"


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
