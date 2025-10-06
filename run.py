from backend.app import create_app
from config import config
from backend.routes.auth import auth_bp
import os

if __name__ == '__main__':
    config_name = os.environ.get('FLASK_ENV') or 'default'
    app = create_app(config[config_name])
    app.run(host='0.0.0.0', port=4000, debug=True)
    app.register_blueprint(auth_bp)