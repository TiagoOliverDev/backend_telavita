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
        
    def get_all_employees(self):
        try:
            employees = self.repository.list_employees()
            return employees
        except Exception as e:
            logging.error(f"Erro ao listar departamentos: {e}")
            return None

    def update_employee(self, employee_id: int, new_name: str):
        if self.repository.exists_employee(new_name):
            return None, 'Nome de departamento já existe'
        
        try:
            if self.repository.update_employee(employee_id, new_name):
                return 'Departamento atualizado com sucesso', True
            else:
                return 'Erro ao atualizar departamento ou departamento não encontrado', False
        except Exception as e:
            logging.error(f"Erro ao editar departamento: {e}")
            return None

    def delete_employee(self, employee_id: int):
        try:
            employee = self.repository.get_employee_by_id(employee_id)
            if not employee:
                return 'Departamento não encontrado', False

            if self.repository.delete_employee(employee_id):
                return 'Departamento excluído com sucesso', True
            else:
                return 'Erro ao excluir o departamento', False
        except Exception as e:
            logging.error(f"Erro ao tentar excluir o departamento: {e}")
            return 'Erro interno ao tentar excluir o departamento', False
           
    def get_employee_by_id(self, employee_id: int):
        try:
            employee = self.repository.get_employee_by_id(employee_id)
            if employee:
                return {'id': employee.id, 'name': employee.name}, True
            else:
                return 'Departamento não encontrado', False
        except Exception as e:
            logging.error(f"Erro ao buscar o departamento por ID: {e}")
            return 'Erro interno ao buscar o departamento', False
        

