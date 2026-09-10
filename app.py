from flask import Flask

from config import Config
from models import db

from routes.auth import auth_bp
from routes.user import user_bp
from routes.officer import officer_bp
from routes.admin import admin_bp
from routes.pothole import pothole_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # Database
    db.init_app(app)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(officer_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(pothole_bp)

    @app.route("/")
    def home():
        return "Pothole Detection PWA API Running"


    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )