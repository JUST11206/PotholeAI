from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .pothole import Pothole
from .pothole_verification import PotholeVerification