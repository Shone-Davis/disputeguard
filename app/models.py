from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import JSONB

from app import db


def utcnow():
    return datetime.now(timezone.utc)


class Dispute(db.Model):
    __tablename__ = "disputes"

    id = db.Column(db.Integer, primary_key=True)
    paypal_dispute_id = db.Column(
        db.String(64), unique=True, nullable=False, index=True)
    reason = db.Column(db.String(64))
    status = db.Column(db.String(64))
    stage = db.Column(db.String(32))  # INQUIRY, CHARGEBACK, ...
    amount = db.Column(db.Numeric(12, 2))
    currency = db.Column(db.String(3))
    seller_transaction_id = db.Column(db.String(64), index=True)
    seller_response_due = db.Column(db.DateTime(timezone=True))
    allowed_actions = db.Column(JSONB, default=list)
    raw = db.Column(JSONB)  # full PayPal response, for debugging and the agent
    first_seen_at = db.Column(db.DateTime(timezone=True), default=utcnow)
    updated_at = db.Column(db.DateTime(timezone=True),
                           default=utcnow, onupdate=utcnow)


class WebhookEvent(db.Model):
    __tablename__ = "webhook_events"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(64), unique=True, nullable=False)
    event_type = db.Column(db.String(64))
    resource_id = db.Column(db.String(64))
    received_at = db.Column(db.DateTime(timezone=True), default=utcnow)
