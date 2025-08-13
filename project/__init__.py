import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .models import db
from .auth.routes import auth_bp, bcrypt
from .items.routes import items_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../instance', 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = "your-super-secret-key-that-you-should-change"

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(items_bp)
    
    return app