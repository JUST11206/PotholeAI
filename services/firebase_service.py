import os
import firebase_admin

from firebase_admin import credentials

from config import Config


def initialize_firebase():

    if firebase_admin._apps:
        return

    if os.getenv("FIREBASE_PROJECT_ID"):

        private_key = os.getenv(
            "FIREBASE_PRIVATE_KEY"
        ).replace("\\n", "\n")

        firebase_config = {
            "type": "service_account",
            "project_id": os.getenv(
                "FIREBASE_PROJECT_ID"
            ),
            "private_key": private_key,
            "client_email": os.getenv(
                "FIREBASE_CLIENT_EMAIL"
            ),
            "token_uri": "https://oauth2.googleapis.com/token"
        }

        credential = credentials.Certificate(
            firebase_config
        )

    else:

        credential = credentials.Certificate(
            Config.FIREBASE_SERVICE_ACCOUNT
        )

    firebase_admin.initialize_app(
        credential
    )