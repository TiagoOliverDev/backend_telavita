from .db import Db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from ..models import Employee, Dependent
import logging

db = Db()

class EmployeeRepository():
    def __init__(self, db):
        self.db = db

    def create_employee(self, name: str, department_id: int, dependents=None):
        """Adiciona um novo colaborador ao banco de dados, junto com seus dependentes, se houver."""
        try:
            new_employee = Employee(name=name, department_id=department_id)
            self.db.session.add(new_employee)
            self.db.session.flush()  # Flush para obter o ID antes do commit

            if dependents:
                for dependent_name in dependents:
                    new_dependent = Dependent(name=dependent_name, employee_id=new_employee.id)
                    self.db.session.add(new_dependent)

            self.db.session.commit()
            return new_employee.id  
        except Exception as e:
            self.db.session.rollback()
            logging.error(f"Erro ao adicionar o colaborador: {e}")
            return None  

    def get_employees_by_department(self, department_id: int):
        """Retorna todos os colaboradores de um departamento específico, com a flag indicando se possuem dependentes."""
        try:
            employees = (self.db.session.query(Employee, func.count(Dependent.id).label('dependents_count'))
                        .outerjoin(Dependent, Employee.id == Dependent.employee_id)
                        .filter(Employee.department_id == department_id)
                        .group_by(Employee.id)
                        .all())
            if not employees: 
                return []  
            return [{
                'id': emp.Employee.id,
                'name': emp.Employee.name,
                'have_dependents': emp.dependents_count > 0
            } for emp in employees]
        except Exception as e:
            logging.error(f"Erro ao buscar colaboradores do departamento {department_id}: {e}")
            return None  

    def exists_employee(self, name: str):
        """Verifica se um colaborador com o dado nome já existe no banco de dados."""
        return Employee.query.filter_by(name=name).first() is not None
        
    def update_employee(self, employee_id: int, new_name: str = None, new_department_id: int = None, new_dependents: list = None):
        try:
            employee = Employee.query.get(employee_id)
            if not employee:
                return False  

            if new_name:
                employee.name = new_name
            
            if new_department_id is not None:
                employee.department_id = new_department_id

            if new_dependents is not None:
                # Remover dependentes atuais
                Dependent.query.filter_by(employee_id=employee_id).delete()
                # Adicionar novos dependentes
                for dependent_name in new_dependents:
                    new_dependent = Dependent(name=dependent_name, employee_id=employee_id)
                    self.db.session.add(new_dependent)

            self.db.session.commit()
            return True
        except Exception as e:
            self.db.session.rollback()
            logging.error(f"Erro ao atualizar dados do colaborador: {e}")
            return False
            
    def exists_employee_with_different_id(self, name: str, employee_id: int):
        """Verifica se existe um colaborador com o mesmo nome, mas com um ID diferente."""
        employee = Employee.query.filter(Employee.name == name, Employee.id != employee_id).first()
        return employee is not None
    
    def delete_employee(self, employee_id: int):
        try:
            employee = Employee.query.get(employee_id)
            if employee:
                self.db.session.delete(employee)
                self.db.session.commit()
                return True
            return False
        except Exception as e:
            self.db.session.rollback()
            logging.error(f"Erro ao excluir o departamento: {e}")
            return False
        
    def get_employee_by_id(self, employee_id: int):
        try:
            employee = Employee.query.get(employee_id)
            if employee:
                return employee
            else:
                return None
        except Exception as e:
            logging.error(f"Erro ao buscar o departamento: {e}")
            return None
        

