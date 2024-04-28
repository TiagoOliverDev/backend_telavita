from flask import request, jsonify, Blueprint
from ..repositories import EmployeeRepository
from ..services.employee_service import EmployeeService
from .resouces.validated_token import token_required
from flask_cors import CORS, cross_origin
from .resouces.cors_preflight_response import CorsOptions
from ..models import db
from ..swagger import EmployeeDocstrings
import logging


employee_repository = EmployeeRepository(db=db)
employee_service = EmployeeService(employee_repository)

employee_blueprint = Blueprint("colaborador", __name__, url_prefix="/colaborador")
cors_options = CorsOptions()


@employee_blueprint.route('/cadastrar', methods=['POST'])
def create_employee():
    try:
        data = request.get_json()
        name = data.get('name')
        department_id = data.get('department_id')
        dependents = data.get('dependents', [])  # Pode ser uma lista ou nulo, padrão é lista vazia

        if not name or department_id is None: 
            return jsonify({'error': 'Nome e departamento são obrigatórios'}), 400
        
        employee_id, message = employee_service.create_employee(name, department_id, dependents)
        
        if employee_id:
            return jsonify({'message': message, 'employee_id': employee_id}), 201
        else:
            return jsonify({'error': message}), 409 if message == 'Colaborador já existe' else 500

    except Exception as e:
        logging.error(f"Erro interno no servidor ao tentar adicionar colaborador: {str(e)}")
        return jsonify({'error': 'Erro interno no servidor'}), 500
    
@employee_blueprint.route('/departamento/<int:department_id>/colaboradores', methods=['GET'])
def get_employees_by_department(department_id: int):
    try:
        employees = employee_service.get_employees_by_department(department_id)
        if employees is not None:
            if employees:  
                return jsonify(employees), 200
            else:
                return jsonify({'error': 'Nenhum colaborador encontrado'}), 404
        else:
            return jsonify({'error': 'Erro ao acessar o banco de dados'}), 500

    except Exception as e:
        logging.error(f"Erro interno no servidor ao tentar listar colaboradores: {str(e)}")
        return jsonify({'error': 'Erro interno no servidor'}), 500

@employee_blueprint.route('/editar/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id: int):
    try:
        data = request.get_json()
        new_name = data.get('name')
        new_department_id = data.get('department_id', None)  
        new_dependents = data.get('dependents', None)  

        if not new_name and new_department_id is None and new_dependents is None:
            return jsonify({'error': 'Nenhuma informação fornecida para atualização'}), 400

        updated_employee_id, message = employee_service.update_employee(employee_id, new_name, new_department_id, new_dependents)

        if updated_employee_id:
            return jsonify({'message': message, 'department_id': updated_employee_id}), 200
        elif message == 'Nome de colaborador já existe':
            return jsonify({'error': message}), 409
        else:
            return jsonify({'error': message}), 500
        
    except Exception as e:
        logging.error(f"Erro interno no servidor ao tentar atualizar colaborador: {str(e)}")
        return jsonify({'error': 'Erro interno no servidor'}), 500
    
@employee_blueprint.route('/excluir/<int:employee_id>', methods=['DELETE'])
def delete_department(employee_id: int):
    try:
        message, success = employee_service.delete_employee(employee_id)
        
        if success:
            return jsonify({'message': message}), 200
        else:
            if message == 'Colaborador não encontrado':
                return jsonify({'error': message}), 404  
            else:
                return jsonify({'error': message}), 500  
    except Exception as e:
        logging.error(f"Erro inesperado ao excluir o colaborador: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@employee_blueprint.route('/busca_por_id/<int:employee_id>', methods=['GET'])
def get_department(employee_id: int):
    try:
        result, success = employee_service.get_employee_by_id(employee_id)
        
        if success:
            return jsonify(result), 200
        else:
            if result == 'employee não encontrado':
                return jsonify({'error': result}), 404
            else:
                return jsonify({'error': result}), 500 
    except Exception as e:
        logging.error(f"Erro inesperado ao buscar o employeeo: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500



############## Integração da docstring para documentar a API via SWAGGER ##############    
create_employee.__doc__ = EmployeeDocstrings.create_employee
get_employees_by_department.__doc__ = EmployeeDocstrings.get_employees_by_department
update_employee.__doc__ = EmployeeDocstrings.update_employee
delete_department.__doc__ = EmployeeDocstrings.delete_department
get_department.__doc__ = EmployeeDocstrings.get_department
