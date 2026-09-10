from datetime import datetime

from . import db


class Pothole(db.Model):

    __tablename__ = "potholes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    image_path = db.Column(
        db.String(500)
    )

    latitude = db.Column(
        db.Float,
        nullable=False
    )

    longitude = db.Column(
        db.Float,
        nullable=False
    )

    confidence = db.Column(
        db.Float
    )

    severity = db.Column(
        db.String(30),
        default="medium"
    )

    priority_score = db.Column(
        db.Float,
        default=0
    )

    priority = db.Column(
        db.String(30),
        default="medium"
    )

    status = db.Column(
        db.String(30),
        default="reported"
    )

    description = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )