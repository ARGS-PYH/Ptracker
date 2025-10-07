from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from backend.database import db, migrate

def create_app(config_class):
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    CORS(app)

    # Landing page route
    @app.route('/')
    def index():
        return render_template('index.html')

    # Health check endpoint
    @app.route('/api')
    def api_status():
        return jsonify({'message': 'API is working', 'status': 'success'}), 200
    
    # Register blueprints
    from backend.routes.auth import auth_bp
    from backend.routes.transactions import transactions_bp  # 👈 NEW

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')  # 👈 NEW

    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
