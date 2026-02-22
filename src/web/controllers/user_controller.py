from flask import Blueprint, request, jsonify
from src.services.user_service import UserService

user_bp = Blueprint('user_controller', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    user_service = UserService()
    data = request.get_json()
    user = user_service.create_user(
        data.get('username'),
        data.get('password'),
        data.get('email')
    )

    if user:
        return jsonify({'message': 'User registered successfully'}), 201
    return jsonify({'message': 'User registration failed'}), 400


@user_bp.route('/login', methods=['POST'])
def login():
    user_service = UserService()
    data = request.get_json()
    token = user_service.sign_in(data.get('username'), data.get('password'))

    if token:
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401