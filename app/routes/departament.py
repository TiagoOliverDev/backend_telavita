from flask import request, jsonify, Blueprint
from ..repositories import DepartamentRepository
from ..services.departament_service import DepartmentService
from .resouces.validated_token import token_required
from flask_cors import CORS, cross_origin
from .resouces.cors_preflight_response import CorsOptions
from ..models import db
import logging


departament_repository = DepartamentRepository(db=db)
departament_service = DepartmentService(departament_repository)

departament_blueprint = Blueprint("departament", __name__, url_prefix="/departament")
cors_options = CorsOptions()


@departament_blueprint.route('/cadastrar', methods=['POST'])
def create_department():
    data = request.get_json()
    department_name = data.get('name')
    
    if not department_name:
        return jsonify({'error': 'O nome do departamento é obrigatório'}), 400
    
    department_id, message = departament_service.create_department(department_name)
    
    if department_id:
        return jsonify({'message': message, 'department_id': department_id}), 201
    elif message == 'Departamento já existe':
        return jsonify({'error': message}), 409  
    else:
        return jsonify({'error': message}), 500
    
@departament_blueprint.route('/listar', methods=['GET'])
def list_departments():
    try:
        departments = departament_service.get_all_departments()
        if departments is None:
            return jsonify({'error': 'Erro ao recuperar departamentos!'}), 500
        
        departments_data = [{'id': d.id, 'name': d.name} for d in departments]
        return jsonify(departments_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@departament_blueprint.route('/editar/<int:department_id>', methods=['PUT'])
def update_department(department_id: int):
    data = request.get_json()
    new_name = data.get('name')
    
    if not new_name:
        return jsonify({'error': 'O novo nome do departamento é obrigatório'}), 400
    
    department_id, message = departament_service.update_department(department_id, new_name)
    
    if department_id:
        return jsonify({'message': message, 'department_id': department_id}), 201
    elif message == 'Nome de departamento já existe':
        return jsonify({'error': message}), 409  
    else:
        return jsonify({'error': message}), 500
    
@departament_blueprint.route('/excluir/<int:department_id>', methods=['DELETE'])
def delete_department(department_id: int):
    try:
        message, success = departament_service.delete_department(department_id)
        
        if success:
            return jsonify({'message': message}), 200
        else:
            if message == 'Departamento não encontrado':
                return jsonify({'error': message}), 404  
            else:
                return jsonify({'error': message}), 500  
    except Exception as e:
        logging.error(f"Erro inesperado ao excluir o departamento: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@departament_blueprint.route('/busca_por_id/<int:department_id>', methods=['GET'])
def get_department(department_id: int):
    try:
        result, success = departament_service.get_department_by_id(department_id)
        
        if success:
            return jsonify(result), 200
        else:
            if result == 'Departamento não encontrado':
                return jsonify({'error': result}), 404
            else:
                return jsonify({'error': result}), 500 
    except Exception as e:
        logging.error(f"Erro inesperado ao buscar o departamento: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

