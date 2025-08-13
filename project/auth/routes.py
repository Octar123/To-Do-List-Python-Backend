from flask import request, jsonify, Blueprint
from project.models import db, User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth',__name__)

bcrypt = Bcrypt()

@auth_bp.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user_exists = User.query.filter_by(username=username).first() is not None
    if user_exists:
        return jsonify({"error": "Username already exists"}), 409
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User '{username}' created Successfully"}), 201

@auth_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        return jsonify({'message' : "Login Successfull",
                        'access_token' : access_token})
    
    return jsonify({"error": "Invalid UserName or Password"}), 401

