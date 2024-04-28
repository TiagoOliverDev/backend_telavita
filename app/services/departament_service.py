# service.py
from ..repositories import DepartamentRepository
import jwt
import logging

# departament_repository = DepartamentRepository()

class DepartmentService:
    def __init__(self, repository):
        self.repository = repository

    def create_department(self, name: str):
        if self.repository.exists_department(name):
            return None, 'Departamento já existe'
        
        try:
            department_id = self.repository.create_department(name)
            if department_id:
                return department_id, 'Departamento criado com sucesso'
            else:
                return None, 'Falha ao criar departamento. O departamento já existe!'
        except Exception as e:
            logging.error(f"Erro ao cadastrar departamento: {e}")
            return None
        
    def get_all_departments(self):
        return self.repository.list_departments()
    

    def update_department(self, department_id: int, new_name: str):
        if self.repository.update_department(department_id, new_name):
            return 'Departamento atualizado com sucesso', True
        else:
            return 'Erro ao atualizar departamento ou departamento não encontrado', False


    def delete_department(self, department_id: int):
        if self.repository.delete_department(department_id):
            return 'Departamento excluído com sucesso', True
        else:
            return 'Erro ao excluir departamento ou departamento não encontrado', False
        
    def get_department_by_id(self, department_id: int):
        department = self.repository.get_department_by_id(department_id)
        if department:
            return {'id': department.id, 'name': department.name}, True
        else:
            return 'Departamento não encontrado', False