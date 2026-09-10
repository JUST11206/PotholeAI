import firebase_admin

from firebase_admin import credentials

from config import Config


def initialize_firebase():

    if firebase_admin._apps:
        return

    credential = credentials.Certificate(
        Config.FIREBASE_SERVICE_ACCOUNT
    )

    firebase_admin.initialize_app(
        credential
    )