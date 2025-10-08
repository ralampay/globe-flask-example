from flask import Flask
from flask_cors import CORS
from flask import jsonify
import os
import yaml
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(env=None):
    app = Flask(__name__)

    # enable CORS for all routes
    CORS(app)

    # -- Load database config ---
    config_path = os.path.join(
        os.path.dirname(__file__),
        "config",
        "database.yml"
    )

    with open(config_path, "r") as f:
        db_configs = yaml.safe_load(f)

    # Choose environment
    env = env or os.getenv("FLASK_ENV", "development")
    db_uri = db_configs[env]["uri"]

    # Path hack
    if db_uri.startswith("sqlite:///"):
        # Remove 'sqlite:///' prefix
        relative_path = db_uri.replace("sqlite:///", "")

        # Resolve absolute path
        abs_path = os.path.join(
            app.root_path, 
            "..",
            relative_path
        )

        # Ensure that the directory exists
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

        # Rebuild full absolute URI
        db_uri = f"sqlite:///{abs_path}"

    print(f"Using database: {db_uri}")

    # Configure SQL Alchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    # Middleware for database config
    db.init_app(app)
    migrate.init_app(app, db)

    from . import models
    from .routes import api
    from .controllers.users_controllers import users_bp
    
    app.register_blueprint(api)
    app.register_blueprint(users_bp)

    # 404: Not found
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "status": "error",
            "message": "not found"
        }), 404

    # 500: Server error
    @app.errorhandler(500)
    def internal_error(e):
        pass

    return app