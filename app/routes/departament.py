from flask import request, jsonify, Blueprint
from ..repositories import DepartamentRepository
from ..services.departament_service import DepartmentService
from .resouces.validated_token import token_required
from flask_cors import CORS, cross_origin
from .resouces.cors_preflight_response import CorsOptions
from ..models import db
import os


SECRET_KEY = os.environ.get('SECRET_KEY')
# departament_service = departamentService(SECRET_KEY)

departament_repository = DepartamentRepository(db=db)
departament_service = DepartmentService(departament_repository)

departament_blueprint = Blueprint("departament", __name__, url_prefix="/departament")
cors_options = CorsOptions()


@departament_blueprint.route('/criar', methods=['POST'])
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
    
@departament_blueprint.route('/list', methods=['GET'])
def list_departments():
    # repo = DepartmentRepository(db)
    departments = departament_repository.list_departments()
    departments_data = [{'id': d.id, 'name': d.name} for d in departments]
    return jsonify(departments_data)


@departament_blueprint.route('/editar/<int:department_id>', methods=['PUT'])
def update_department(department_id: int):
    data = request.get_json()
    new_name = data.get('name')
    
    if not new_name:
        return jsonify({'error': 'O novo nome do departamento é obrigatório'}), 400
    
    message, success = departament_service.update_department(department_id, new_name)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 404  
    

@departament_blueprint.route('/excluir/<int:department_id>', methods=['DELETE'])
def delete_department(department_id: int):
    message, success = departament_service.delete_department(department_id)
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 404  # ou 500, dependendo da lógica específica
    

@departament_blueprint.route('/buscar/<int:department_id>', methods=['GET'])
def get_department(department_id: int):
    result, success = departament_service.get_department_by_id(department_id)
    
    if success:
        return jsonify(result), 200
    else:
        return jsonify({'error': result}), 404

# @departament_blueprint.route('/list_all_departaments', methods=['GET'])
# @token_required
# def list_all_departaments(current_user):
#     departaments = departament_service.list_all_departaments()
#     if departaments is None:
#         return jsonify({'message': 'Error fetching departaments'}), 500
    
#     return jsonify({'departaments': departaments}), 200


# @departament_blueprint.route('/register_departament', methods=['POST', 'OPTIONS'])
# # @token_required
# @cross_origin(origin='*', headers=['Content-Type', 'Authorization']) 
# def register_departament():

#     if request.method == 'OPTIONS':
#         return cors_options._build_cors_preflight_response()
    
#     if request.method == 'POST':
#         data = request.get_json()
#         name = data['nomeSetor']

#         if not all([name]):
#             return jsonify({'message': 'Field is required'}), 400

#         departament, error = departament_service.register_departament(name=name)
#         if error:
#             return jsonify({'message': error}), 400

#         return jsonify({'departament': departament, 'message': 'departament created successfully'}), 201


# @departament_blueprint.route('/departament/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @token_required
# def departament(current_user, id):
#     if request.method == 'GET':
#         departament, error = departament_service.list_departament_by_id(id=id)
#         if error:
#             return jsonify({'message': error}), 500
#         if not departament:
#             return jsonify({'message': 'departament not found'}), 404
        
#         return jsonify({'departament': [departament] if departament else [None]}), 200

#     elif request.method == 'PUT':
#         data = request.get_json()
#         if 'nomeSetor' not in data:
#             return jsonify({'message': 'nomeSetor is required'}), 400

#         name = data['nomeSetor']

#         updated_departament, error = departament_service.update_departament(id=id, name=name)
#         if error:
#             return jsonify({'message': error}), 500
#         if not updated_departament:
#             return jsonify({'message': 'departament not found'}), 404
        
#         return jsonify({'departament': updated_departament}), 200

#     elif request.method == 'DELETE':
#         success, error = departament_service.departament_delete(id=id)
#         if error:
#             return jsonify({'message': error}), 500
#         if not success:
#             return jsonify({'message': 'departament not found'}), 404
        
#         return jsonify({'message': 'departament deleted successfully'}), 200