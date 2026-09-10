from flask import (
    Blueprint,
    render_template,
    jsonify,
    request
)
from models.pothole_verification import PotholeVerification
from models.pothole import Pothole
from utils.decorators import role_required


officer_bp = Blueprint(
    "officer",
    __name__,
    url_prefix="/officer"
)

@officer_bp.route("/dashboard")
@role_required("officer")
def dashboard():

    potholes = Pothole.query.order_by(
        Pothole.created_at.desc()
    ).all()

    total_reports = Pothole.query.count()

    critical_count = Pothole.query.filter_by(
        priority="critical"
    ).count()

    high_count = Pothole.query.filter_by(
        priority="high"
    ).count()

    pending_count = Pothole.query.filter(
        Pothole.status != "resolved"
    ).count()

    total_verifications = (
        PotholeVerification.query.count()
    )

    verified_reports = 0

    for pothole in potholes:

        verification_count = (
            PotholeVerification.query
            .filter_by(
                pothole_id=pothole.id
            )
            .count()
        )

        if verification_count >= 2:
            verified_reports += 1

    return render_template(
        "officer/dashboard.html",
        potholes=potholes,
        total_reports=total_reports,
        critical_count=critical_count,
        high_count=high_count,
        pending_count=pending_count,
        total_verifications=total_verifications,
        verified_reports=verified_reports
    )

@officer_bp.route("/map")
#@role_required("officer")
def map():

    return render_template(
        "officer/map.html"
    )

@officer_bp.route("/api/potholes")
#@role_required("officer")
def pothole_api():

    potholes = Pothole.query.order_by(
        Pothole.created_at.desc()
    ).all()

    data = []

    for p in potholes:

        verification_count = PotholeVerification.query.filter_by(
            pothole_id=p.id
        ).count()

        data.append({
            "id": p.id,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "severity": p.severity,
            "priority": p.priority,
            "priority_score": p.priority_score,
            "confidence": p.confidence,
            "status": p.status,
            "verification_count": verification_count
        })

    return jsonify(data)

@officer_bp.route("/potholes")
@role_required("officer")
def potholes():

    potholes = Pothole.query.order_by(
        Pothole.created_at.desc()
    ).all()

    return render_template(
        "officer/potholes.html",
        potholes=potholes
    )

@officer_bp.route("/pothole/<int:pothole_id>")
@role_required("officer")
def pothole_details(pothole_id):

    pothole = Pothole.query.get_or_404(
        pothole_id
    )

    verification_count = (
        PotholeVerification.query
        .filter_by(
            pothole_id=pothole.id
        )
        .count()
    )

    return render_template(
        "officer/pothole-details.html",
        pothole=pothole,
        verification_count=verification_count
    )

@officer_bp.route(
    "/pothole/<int:pothole_id>/status",
    methods=["POST"]
)
@role_required("officer")
def update_pothole_status(pothole_id):

    pothole = Pothole.query.get_or_404(
        pothole_id
    )

    data = request.get_json()

    new_status = data.get("status")

    allowed_statuses = [
        "reported",
        "under_review",
        "in_progress",
        "resolved"
    ]

    if new_status not in allowed_statuses:

        return jsonify({
            "success": False,
            "message": "Invalid status"
        }), 400

    pothole.status = new_status

    from models import db

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Status updated successfully",
        "status": pothole.status
    })