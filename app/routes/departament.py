from flask import request, jsonify, Blueprint
from ..repositories import DepartamentRepository
from ..services.departament_service import DepartmentService
from .resouces.validated_token import token_required
from flask_cors import CORS, cross_origin
from .resouces.cors_preflight_response import CorsOptions
from ..models import db
from ..swagger import DepartmentDocstrings
import logging


departament_repository = DepartamentRepository(db=db)
departament_service = DepartmentService(departament_repository)

departament_blueprint = Blueprint("departament", __name__, url_prefix="/departament")
cors_options = CorsOptions()


@departament_blueprint.route('/cadastrar', methods=['POST'])
def create_department():
    """
    Cadastra um novo departamento.
    
    Recebe o nome do departamento via JSON e tenta criá-lo. Retorna uma mensagem de sucesso com o ID
    do departamento criado, uma mensagem de erro se o departamento já existir, ou um erro genérico se
    ocorrer outra falha.
    
    Returns:
        JSON response with status code.
    """
    data = request.get_json()
    department_name = data.get('name')

    if not department_name:
        return jsonify({'error': 'O nome do departamento é obrigatório'}), 400

    try:
        department_id, message = departament_service.create_department(department_name)

        if department_id:
            return jsonify({'message': message, 'department_id': department_id}), 201
        elif message == 'Departamento já existe':
            return jsonify({'error': message}), 409
        else:
            return jsonify({'error': 'Erro ao tentar criar o departamento'}), 500
    except Exception as e:
        logging.error(f"Erro inesperado ao criar o departamento: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
    
@departament_blueprint.route('/listar', methods=['GET'])
def list_departments():
    """
    Lista todos os departamentos cadastrados.
    
    Tenta recuperar todos os departamentos e devolve uma lista contendo seus dados. Se houver uma falha,
    retorna um erro genérico.
    
    Returns:
        JSON response with status code.
    """
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
    """
    Atualiza o nome de um departamento existente.
    
    Recebe um novo nome para o departamento via JSON. Se o novo nome não for fornecido, retorna um erro.
    Se a atualização for bem-sucedida, retorna sucesso; se o nome já existir, retorna um erro específico;
    caso contrário, retorna um erro genérico.
    
    Args:
        department_id (int): ID do departamento a ser atualizado.

    Returns:
        JSON response with status code.
    """
    data = request.get_json()
    new_name = data.get('name')

    if not new_name:
        return jsonify({'error': 'O novo nome do departamento é obrigatório'}), 400

    try:
        updated_department_id, message = departament_service.update_department(department_id, new_name)

        if updated_department_id:
            return jsonify({'message': message, 'department_id': updated_department_id}), 200  
        elif message == 'Nome de departamento já existe':
            return jsonify({'error': message}), 409
        else:
            return jsonify({'error': 'Erro ao tentar atualizar o departamento'}), 500
    except Exception as e:
        logging.error(f"Erro inesperado ao atualizar o departamento: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
    
@departament_blueprint.route('/excluir/<int:department_id>', methods=['DELETE'])
def delete_department(department_id: int):
    """
    Exclui um departamento existente.
    
    Tenta excluir um departamento com base no ID fornecido. Se o departamento for excluído com sucesso,
    retorna uma mensagem de sucesso; se não for encontrado, retorna um erro específico; caso contrário, retorna
    um erro genérico.
    
    Args:
        department_id (int): ID do departamento a ser excluído.

    Returns:
        JSON response with status code.
    """
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
    """
    Busca um departamento por ID.
    
    Tenta encontrar um departamento pelo ID fornecido. Se encontrado, retorna os dados do departamento;
    se não for encontrado, retorna um erro específico; em caso de outra falha, retorna um erro genérico.
    
    Args:
        department_id (int): ID do departamento a ser buscado.

    Returns:
        JSON response with status code.
    """
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



############## Integração da docstring para documentar a API via SWAGGER ##############
create_department.__doc__ = DepartmentDocstrings.create_department
list_departments.__doc__ = DepartmentDocstrings.list_departments
update_department.__doc__ = DepartmentDocstrings.update_departments
delete_department.__doc__ = DepartmentDocstrings.delete_department
get_department.__doc__ = DepartmentDocstrings.get_department_by_id

