from flask import Flask, request, jsonify, Blueprint
from ..repositories.auth_repository import AuthRepository
from ..services.auth_service import AuthService
from flask_bcrypt import Bcrypt
import os


SECRET_KEY = os.environ.get('SECRET_KEY')
auth_service = AuthService(SECRET_KEY)
auth_repository = AuthRepository()

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    name = data['name']
    email = data['email']
    password = data['senha']
    matricula = data['matricula']
    tipo_permissao = 2 # 2 = usuário admin
    # tipo_permissao = data['tipo_permissao']

    if not all([name, email, password, matricula, tipo_permissao]):
        return jsonify({'message': 'All fields are required'}), 400

    user, error = auth_service.register_user(name, email, password, matricula, tipo_permissao)
    if error:
        return jsonify({'message': error}), 400

    return jsonify({'user': user, 'message': 'User created successfully'}), 201





