from flask import (
    Blueprint,
    render_template,
    session
)

from utils.decorators import login_required
from models.pothole import Pothole

user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/user"
)


@user_bp.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "user/dashboard.html"
    )

# @user_bp.route("/reports")
# @login_required
# def reports():

#     user_id = session.get("user_id")

#     potholes = Pothole.query.filter_by(
#         user_id=user_id
#     ).order_by(
#         Pothole.created_at.desc()
#     ).all()

#     return render_template(
#         "user/reports.html",
#         potholes=potholes
#     )

@user_bp.route("/reports")
@login_required
def reports():

    user_id = session.get("user_id")

    print("DEBUG USER ID:", user_id)

    potholes = Pothole.query.filter_by(
        user_id=user_id
    ).order_by(
        Pothole.created_at.desc()
    ).all()

    print("DEBUG POTHOLES:", potholes)

    return render_template(
        "user/reports.html",
        potholes=potholes
    )

@user_bp.route("/report")
@login_required
def report():
    return render_template(
        "user/report.html"
    )

@user_bp.route("/map")
@login_required
def pothole_map():

    return render_template(
        "user/map.html"
    )