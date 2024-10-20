# app/routes/user_routes.py

from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from flask_cors import cross_origin

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')

@user_bp.route('/', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        user_data = {
            'id': user.id,
            'login_id': user.login_id,
            'name': user.name,
            'role': user.role
        }
        result.append(user_data)
    return jsonify(result), 200

@user_bp.route('/<int:id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_user(id):
    user = User.query.get_or_404(id)
    user_data = {
        'id': user.id,
        'login_id': user.login_id,
        'name': user.name,
        'role': user.role
    }
    return jsonify(user_data), 200

@user_bp.route('/', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    login_id = data.get('login_id')
    password = data.get('password')
    name = data.get('name')
    role = data.get('role')

    if not all([login_id, password, name, role]):
        return jsonify({'message': 'Missing required fields'}), 400

    if User.query.filter_by(login_id=login_id).first():
        return jsonify({'message': 'User with this login_id already exists'}), 400

    user = User(
        login_id=login_id,
        name=name,
        role=role
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created', 'id': user.id}), 201

@user_bp.route('/<int:id>', methods=['PUT'])
@cross_origin(supports_credentials=True)
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    login_id = data.get('login_id', user.login_id)
    name = data.get('name', user.name)
    role = data.get('role', user.role)
    password = data.get('password', None)

    if login_id != user.login_id and User.query.filter_by(login_id=login_id).first():
        return jsonify({'message': 'User with this login_id already exists'}), 400

    user.login_id = login_id
    user.name = name
    user.role = role

    if password:
        user.set_password(password)

    db.session.commit()
    return jsonify({'message': 'User updated'}), 200

@user_bp.route('/<int:id>', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200