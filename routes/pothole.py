import os

from flask import (
    Blueprint,
    request,
    jsonify,
    session
)

from models import db
from models.pothole import Pothole
from models.pothole_verification import PotholeVerification
from services.pothole_service import analyze_pothole


pothole_bp = Blueprint(
    "pothole",
    __name__,
    url_prefix="/api/pothole"
)


UPLOAD_FOLDER = "uploads"


@pothole_bp.route(
    "/report",
    methods=["POST"]
)
def report_pothole():

    if "user_id" not in session:

        return jsonify({
            "success": False,
            "message": "Login required"
        }), 401

    image = request.files.get(
        "image"
    )

    latitude = request.form.get(
        "latitude",
        type=float
    )

    longitude = request.form.get(
        "longitude",
        type=float
    )

    if not image:

        return jsonify({
            "success": False,
            "message": "Image required"
        }), 400

    if latitude is None or longitude is None:

        return jsonify({
            "success": False,
            "message": "GPS location required"
        }), 400

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    filename = image.filename

    path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    image.save(path)

    result = analyze_pothole(path)

    if not result["detected"]:

        return jsonify({
            "success": False,
            "message": "No pothole detected"
        })

    pothole = Pothole(
        user_id=session["user_id"],
        image_path=path,
        latitude=latitude,
        longitude=longitude,
        confidence=result["confidence"],
        severity=result["severity"],
        priority_score=result["priority_score"],
        priority=result["priority"],
        status="reported",
        description=result["description"],
    )

    db.session.add(pothole)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Pothole reported",
        "pothole_id": pothole.id,
        "severity": pothole.severity,
        "priority": pothole.priority,
        "priority_score": pothole.priority_score
    })
@pothole_bp.route("/all", methods=["GET"])
def get_all_potholes():

    potholes = Pothole.query.order_by(
        Pothole.created_at.desc()
    ).all()

    data = []

    for pothole in potholes:

        verification_count = PotholeVerification.query.filter_by(
            pothole_id=pothole.id
        ).count()

        data.append({
            "id": pothole.id,
            "latitude": pothole.latitude,
            "longitude": pothole.longitude,
            "severity": pothole.severity,
            "priority": pothole.priority,
            "priority_score": pothole.priority_score,
            "status": pothole.status,
            "description": pothole.description,
            "verification_count": verification_count,
            "created_at": (
                pothole.created_at.isoformat()
                if pothole.created_at
                else None
            )
        })

    return jsonify({
        "success": True,
        "potholes": data
    })

@pothole_bp.route(
    "/<int:pothole_id>/verify",
    methods=["POST"]
)
def verify_pothole(pothole_id):

    # Login check
    if "user_id" not in session:

        return jsonify({
            "success": False,
            "message": "Login required"
        }), 401

    user_id = session["user_id"]

    # Check pothole exists
    pothole = Pothole.query.get(pothole_id)

    if not pothole:

        return jsonify({
            "success": False,
            "message": "Pothole not found"
        }), 404

    # Check if this user already verified this pothole
    existing_verification = (
        PotholeVerification.query
        .filter_by(
            pothole_id=pothole_id,
            user_id=user_id
        )
        .first()
    )

    if existing_verification:

        return jsonify({
            "success": False,
            "already_verified": True,
            "message": "You have already verified this pothole."
        }), 400

    # Create verification
    verification = PotholeVerification(
        pothole_id=pothole_id,
        user_id=user_id
    )

    db.session.add(verification)

    # Save verification first
    db.session.commit()

    # Count total verifications
    verification_count = (
        PotholeVerification.query
        .filter_by(
            pothole_id=pothole_id
        )
        .count()
    )

    # Increase priority score
    pothole.priority_score = min(
        100,
        (pothole.priority_score or 0) + 2
    )

    # Update priority level
    if pothole.priority_score >= 80:
        pothole.priority = "critical"

    elif pothole.priority_score >= 60:
        pothole.priority = "high"

    elif pothole.priority_score >= 30:
        pothole.priority = "medium"

    else:
        pothole.priority = "low"

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Pothole verified successfully",
        "verification_count": verification_count,
        "priority_score": pothole.priority_score,
        "priority": pothole.priority
    })