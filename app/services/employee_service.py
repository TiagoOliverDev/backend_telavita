import logging

class EmployeeService:
    def __init__(self, repository):
        self.repository = repository

    def create_employee(self, name: str, department_id: int, dependents=None):
        """Chama o repositório para adicionar um novo colaborador e seus dependentes, se houver."""
        if self.repository.exists_employee(name):
            return None, 'Colaborador já existe'
        
        try:
            employee_id = self.repository.create_employee(name, department_id, dependents)
            if employee_id:
                return employee_id, 'Colaborador adicionado com sucesso'
            else:
                return None
        except Exception as e:
            logging.error(f"Erro ao cadastrar colaborador: {e}")
            return None

    def get_employees_by_department(self, department_id: int):
        """Busca todos os colaboradores de um departamento com detalhes sobre dependentes."""
        try:
            employees = self.repository.get_employees_by_department(department_id)
            if employees is not None:  
                return employees
            else:
                return None  
        except Exception as e:
            logging.error(f"Erro ao listar colaboradores: {e}")
            return None
        
    def update_employee(self, employee_id: int, new_name: str = None, new_department_id: int = None, new_dependents: list = None):
        try:
            if new_name and self.repository.exists_employee_with_different_id(new_name, employee_id):
                return None, 'Nome de colaborador já existe'

            if self.repository.update_employee(employee_id, new_name, new_department_id, new_dependents):
                return employee_id, 'Colaborador atualizado com sucesso'
            else:
                return 'Erro ao atualizar colaborador ou colaborador não encontrado', False
        except Exception as e:
            logging.error(f"Erro ao atualizar colaborador: {e}")
            return None

    def delete_employee(self, employee_id: int):
        try:
            employee = self.repository.get_employee_by_id(employee_id)
            if not employee:
                return 'Colaborador não encontrado', False

            if self.repository.delete_employee(employee_id):
                return 'Colaborador excluído com sucesso', True
            else:
                return 'Erro ao excluir o colaborador', False
        except Exception as e:
            logging.error(f"Erro ao tentar excluir o colaborador: {e}")
            return 'Erro interno ao tentar excluir o colaborador', False
           
    def get_employee_by_id(self, employee_id: int):
        try:
            employee_data = self.repository.get_employee_by_id(employee_id)
            if employee_data:
                return employee_data, True
            else:
                return 'Colaborador não encontrado', False
        except Exception as e:
            logging.error(f"Erro ao buscar o colaborador por ID: {e}")
            return 'Erro interno ao buscar o colaborador', False
        

