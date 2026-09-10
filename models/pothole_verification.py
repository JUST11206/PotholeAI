from datetime import datetime
from . import db


class PotholeVerification(db.Model):
    __tablename__ = "pothole_verifications"

    id = db.Column(db.Integer, primary_key=True)

    pothole_id = db.Column(
        db.Integer,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    __table_args__ = (
        db.UniqueConstraint(
            "pothole_id",
            "user_id",
            name="unique_user_pothole"
        ),
    )