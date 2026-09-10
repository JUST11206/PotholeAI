from datetime import datetime

from . import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    firebase_uid = db.Column(
        db.String(128),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="user",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )