from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from src.core.models.user_request import UserRegistrationRequest
from src.services.user_service import UserService

user_bp = Blueprint('user_controller', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    user_service = UserService()
    data = request.get_json()

    try:
        registration_data = UserRegistrationRequest(**data)
        exists_username = user_service.exists(registration_data.username)
        exists_email = user_service.exists(registration_data.email)

        if exists_username:
            return jsonify({"message": "username already in use"}), 400
        if exists_email:
            return jsonify({"message": "email already in use"}), 400

        user = user_service.create_user(
            registration_data.username,
            registration_data.password,
            registration_data.email
        )

        if user:
            return jsonify({"message": "user created"}), 201
        return jsonify({"message": "wrong user credentials format"}), 400

    except (ValidationError, TypeError, ValueError):
        return jsonify({"message": "wrong user credentials format"}), 400


@user_bp.route('/login', methods=['POST'])
def login():
    user_service = UserService()
    data = request.get_json()
    token = user_service.sign_in(data.get('username'), data.get('password'))

    if token:
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401