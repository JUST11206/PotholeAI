import os
from dotenv import load_dotenv


load_dotenv()


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CA_PATH = os.path.join(
    BASE_DIR,
    "certs",
    "ca.pem"
)


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-key"
    )


    # =========================
    # DATABASE
    # =========================

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 1800,
        "pool_timeout": 30,
        "pool_size": 5,
        "max_overflow": 2,

        "connect_args": {
            "ssl_ca": CA_PATH,
            "ssl_verify_cert": True,
            "ssl_verify_identity": True,
            "connect_timeout": 10,
            "read_timeout": 30,
            "write_timeout": 30
        }
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # =========================
    # FIREBASE
    # =========================

    FIREBASE_SERVICE_ACCOUNT = os.path.join(
        BASE_DIR,
        "firebase",
        "pothole-3a10a-firebase-adminsdk-fbsvc-6fa20134d0.json"
    )


    # =========================
    # SMTP
    # =========================

    SMTP_HOST = os.getenv(
        "SMTP_HOST"
    )

    SMTP_PORT = int(
        os.getenv("SMTP_PORT", 587)
    )

    SMTP_USERNAME = os.getenv(
        "SMTP_USERNAME"
    )

    SMTP_PASSWORD = os.getenv(
        "SMTP_PASSWORD"
    )
    #=========================
    OFFICER_CODE = os.getenv(
    "OFFICER_CODE"
)