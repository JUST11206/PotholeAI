
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for
)

from models import db
from models.user import User

from services.firebase_service import initialize_firebase
from services.otp_service import (
    generate_otp,
    save_otp,
    verify_otp,
    send_otp
)

from config import Config

from firebase_admin import auth


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# Initialize Firebase
initialize_firebase()


# =====================================
# CITIZEN LOGIN PAGE
# =====================================

@auth_bp.route("/login")
def login():

    return render_template(
        "auth/login.html"
    )


# =====================================
# CITIZEN SIGNUP PAGE
# =====================================

@auth_bp.route("/signup")
def signup():

    return render_template(
        "auth/signup.html"
    )


# =====================================
# CITIZEN SEND OTP
# =====================================

@auth_bp.route(
    "/send-otp",
    methods=["POST"]
)
def send_otp_route():

    name = request.form.get(
        "name",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    password = request.form.get(
        "password",
        ""
    )


    # Validation
    if not name or not email or not password:

        return "Name, email and password are required.", 400


    if len(password) < 6:

        return "Password must be at least 6 characters.", 400


    # Check existing user
    existing_user = User.query.filter_by(
        email=email
    ).first()


    if existing_user:

        return "An account with this email already exists.", 400


    # Generate OTP
    otp = generate_otp()

    save_otp(
        email,
        otp
    )


    # Store signup information temporarily
    session["signup_name"] = name
    session["signup_email"] = email
    session["signup_password"] = password
    session["signup_role"] = "user"


    try:

        send_otp(
            email,
            otp,
            Config.SMTP_HOST,
            Config.SMTP_PORT,
            Config.SMTP_USERNAME,
            Config.SMTP_PASSWORD
        )

    except Exception as e:

        print(
            "OTP sending error:",
            e
        )

        return "Failed to send OTP. Check SMTP configuration.", 500


    return render_template(
        "auth/verify-otp.html"
    )


# =====================================
# CITIZEN VERIFY OTP
# =====================================

@auth_bp.route(
    "/verify-otp",
    methods=["POST"]
)
def verify_otp_route():

    otp = request.form.get(
        "otp",
        ""
    ).strip()


    email = session.get(
        "signup_email"
    )

    name = session.get(
        "signup_name"
    )

    password = session.get(
        "signup_password"
    )

    role = session.get(
        "signup_role",
        "user"
    )


    if not email or not name or not password:

        return "Signup session expired. Please signup again.", 400


    # Verify OTP
    if not verify_otp(
        email,
        otp
    ):

        return "Invalid OTP.", 400


    try:

        # Create Firebase user
        firebase_user = auth.create_user(
            email=email,
            password=password,
            display_name=name
        )


        # Create TiDB user
        user = User(
            firebase_uid=firebase_user.uid,
            email=email,
            name=name,
            role=role
        )


        db.session.add(user)

        db.session.commit()


        # Login user automatically
        session["user_id"] = user.id
        session["firebase_uid"] = user.firebase_uid
        session["email"] = user.email
        session["name"] = user.name
        session["role"] = user.role


        # Clear signup data
        session.pop(
            "signup_name",
            None
        )

        session.pop(
            "signup_email",
            None
        )

        session.pop(
            "signup_password",
            None
        )

        session.pop(
            "signup_role",
            None
        )


        return redirect(
            url_for(
                "user.dashboard"
            )
        )


    except Exception as e:

        db.session.rollback()

        print(
            "Signup error:",
            e
        )

        return "Account creation failed.", 500


# =====================================
# OFFICER LOGIN PAGE
# =====================================

@auth_bp.route("/officer/login")
def officer_login():

    return render_template(
        "officer/login.html"
    )


# =====================================
# OFFICER SIGNUP PAGE
# =====================================

@auth_bp.route("/officer/signup")
def officer_signup():

    return render_template(
        "officer/signup.html"
    )


# =====================================
# OFFICER SEND OTP
# =====================================

@auth_bp.route(
    "/officer/send-otp",
    methods=["POST"]
)
def officer_send_otp():

    name = request.form.get(
        "name",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    password = request.form.get(
        "password",
        ""
    )

    officer_code = request.form.get(
        "officer_code",
        ""
    ).strip()


    # Basic validation
    if not name or not email or not password or not officer_code:

        return "All fields are required.", 400


    if len(password) < 6:

        return "Password must be at least 6 characters.", 400


    # Check officer registration code
    if officer_code != Config.OFFICER_CODE:

        return "Invalid officer registration code.", 403


    # Check existing user
    existing_user = User.query.filter_by(
        email=email
    ).first()


    if existing_user:

        return "An account with this email already exists.", 400


    # Generate OTP
    otp = generate_otp()

    save_otp(
        email,
        otp
    )


    # Store officer signup information
    session["signup_name"] = name
    session["signup_email"] = email
    session["signup_password"] = password
    session["signup_role"] = "officer"


    try:

        send_otp(
            email,
            otp,
            Config.SMTP_HOST,
            Config.SMTP_PORT,
            Config.SMTP_USERNAME,
            Config.SMTP_PASSWORD
        )

    except Exception as e:

        print(
            "Officer OTP sending error:",
            e
        )

        return "Failed to send OTP. Check SMTP configuration.", 500


    return render_template(
        "officer/verify-otp.html"
    )


# =====================================
# OFFICER VERIFY OTP
# =====================================

@auth_bp.route(
    "/officer/verify-otp",
    methods=["POST"]
)
def officer_verify_otp():

    otp = request.form.get(
        "otp",
        ""
    ).strip()


    email = session.get(
        "signup_email"
    )

    name = session.get(
        "signup_name"
    )

    password = session.get(
        "signup_password"
    )

    role = session.get(
        "signup_role"
    )


    if not email or not name or not password:

        return "Signup session expired. Please signup again.", 400


    # Make sure this OTP belongs to officer signup
    if role != "officer":

        return "Invalid officer signup session.", 403


    # Verify OTP
    if not verify_otp(
        email,
        otp
    ):

        return "Invalid OTP.", 400


    try:

        # Create Firebase officer account
        firebase_user = auth.create_user(
            email=email,
            password=password,
            display_name=name
        )


        # Create officer in TiDB
        user = User(
            firebase_uid=firebase_user.uid,
            email=email,
            name=name,
            role="officer"
        )


        db.session.add(user)

        db.session.commit()


        # Login officer automatically
        session["user_id"] = user.id
        session["firebase_uid"] = user.firebase_uid
        session["email"] = user.email
        session["name"] = user.name
        session["role"] = "officer"


        # Clear signup session
        session.pop(
            "signup_name",
            None
        )

        session.pop(
            "signup_email",
            None
        )

        session.pop(
            "signup_password",
            None
        )

        session.pop(
            "signup_role",
            None
        )


        return redirect(
            url_for(
                "officer.dashboard"
            )
        )


    except Exception as e:

        db.session.rollback()

        print(
            "Officer signup error:",
            e
        )

        return "Officer account creation failed.", 500


# =====================================
# FIREBASE CITIZEN SESSION
# =====================================

@auth_bp.route(
    "/session",
    methods=["POST"]
)
def create_session():

    data = request.get_json()


    if not data:

        return jsonify({
            "success": False,
            "message": "Request data missing"
        }), 400


    id_token = data.get(
        "idToken"
    )


    if not id_token:

        return jsonify({
            "success": False,
            "message": "Firebase ID token missing"
        }), 400


    try:

        decoded_token = auth.verify_id_token(
            id_token
        )


        firebase_uid = decoded_token["uid"]

        email = decoded_token.get(
            "email"
        )


        # Find TiDB user
        user = User.query.filter_by(
            firebase_uid=firebase_uid
        ).first()


        if not user and email:

            user = User.query.filter_by(
                email=email
            ).first()


        if not user:

            return jsonify({
                "success": False,
                "message": "User not registered"
            }), 404


        # Flask session
        session["user_id"] = user.id
        session["firebase_uid"] = user.firebase_uid
        session["email"] = user.email
        session["name"] = user.name
        session["role"] = user.role


        # Redirect according to role
        if user.role == "admin":

            redirect_url = "/admin/dashboard"

        elif user.role == "officer":

            redirect_url = "/officer/dashboard"

        else:

            redirect_url = "/user/dashboard"


        return jsonify({
            "success": True,
            "message": "Login successful",
            "redirect": redirect_url
        })


    except Exception as e:

        print(
            "Firebase authentication error:",
            e
        )


        return jsonify({
            "success": False,
            "message": "Invalid Firebase authentication"
        }), 401


# =====================================
# FIREBASE OFFICER SESSION
# =====================================

@auth_bp.route(
    "/officer/session",
    methods=["POST"]
)
def officer_session():

    data = request.get_json()


    if not data:

        return jsonify({
            "success": False,
            "message": "Request data missing"
        }), 400


    id_token = data.get(
        "idToken"
    )


    if not id_token:

        return jsonify({
            "success": False,
            "message": "Firebase ID token missing"
        }), 400


    try:

        decoded_token = auth.verify_id_token(
            id_token
        )


        firebase_uid = decoded_token["uid"]

        email = decoded_token.get(
            "email"
        )


        # Find user
        user = User.query.filter_by(
            firebase_uid=firebase_uid
        ).first()


        if not user and email:

            user = User.query.filter_by(
                email=email
            ).first()


        if not user:

            return jsonify({
                "success": False,
                "message": "Officer account not registered"
            }), 404


        # IMPORTANT:
        # Only officer can use officer login
        if user.role != "officer":

            return jsonify({
                "success": False,
                "message": "This account is not an officer account."
            }), 403


        # Create Flask session
        session["user_id"] = user.id
        session["firebase_uid"] = user.firebase_uid
        session["email"] = user.email
        session["name"] = user.name
        session["role"] = "officer"


        return jsonify({
            "success": True,
            "message": "Officer login successful",
            "redirect": "/officer/dashboard"
        })


    except Exception as e:

        print(
            "Officer Firebase authentication error:",
            e
        )


        return jsonify({
            "success": False,
            "message": "Invalid officer authentication"
        }), 401


# =====================================
# LOGOUT
# =====================================

@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("auth.login")
    )

