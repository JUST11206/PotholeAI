from flask import (
    Blueprint,
    render_template
)

from models.user import User
from models.pothole import Pothole
from models.pothole_verification import PotholeVerification

from utils.decorators import role_required


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin_bp.route("/dashboard")
#@role_required("admin")
def dashboard():

    # ==============================
    # BASIC COUNTS
    # ==============================

    users = User.query.count()

    potholes = Pothole.query.count()


    # ==============================
    # PRIORITY COUNTS
    # ==============================

    critical = Pothole.query.filter_by(
        priority="critical"
    ).count()


    # ==============================
    # STATUS COUNTS
    # ==============================

    pending = Pothole.query.filter(
        Pothole.status != "resolved"
    ).count()


    resolved = Pothole.query.filter_by(
        status="resolved"
    ).count()


    # ==============================
    # COMMUNITY VERIFICATIONS
    # ==============================

    verifications = (
        PotholeVerification.query.count()
    )


    return render_template(
        "admin/dashboard.html",

        users=users,

        potholes=potholes,

        critical=critical,

        pending=pending,

        resolved=resolved,

        verifications=verifications
    )


@admin_bp.route("/users")
@role_required("admin")
def users():

    users = User.query.all()

    return render_template(
        "admin/users.html",
        users=users
    )


@admin_bp.route("/potholes")
@role_required("admin")
def potholes():

    potholes = Pothole.query.all()

    return render_template(
        "admin/potholes.html",
        potholes=potholes
    )