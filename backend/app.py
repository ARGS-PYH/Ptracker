from flask import Flask, jsonify, render_template
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from backend.database import db, migrate
from backend.models import user
from config import Config


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static",
    )

    # Load configuration
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)
    CORS(app)

    # Landing page
    @app.route("/")
    def index():
        return render_template("index.html")

    # API status check
    @app.route("/api")
    def api_status():
        return jsonify({"message": "API is working", "status": "success"}), 200

    # Register blueprints
    from backend.routes.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app
