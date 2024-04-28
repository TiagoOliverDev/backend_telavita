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

  
    def exists_employee(self, name: str):
        """Verifica se um colaborador com o dado nome já existe no banco de dados."""
        return Employee.query.filter_by(name=name).first() is not None
        
    def list_employees(self):
        try:
            employees = Employee.query.order_by(Employee.id).all()
            return employees
        except Exception as e:
            logging.error(f"Erro ao listar departamentos: {e}")
            return []
        
    def update_employee(self, employee_id: int, new_name: str):
        try:
            employee = Employee.query.get(employee_id)
            if employee:
                employee.name = new_name
                self.db.session.commit()
                return True
            return False
        except Exception as e:
            self.db.session.rollback()
            logging.error(f"Erro ao atualizar o departamento: {e}")
            return False
        
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
        
    def get_employees_by_department(self, department_id: int):
        """Retorna todos os colaboradores de um departamento específico, com a flag indicando se possuem dependentes."""
        try:
            employees = (self.db.session.query(Employee, func.count(Dependent.id).label('dependents_count'))
                        .outerjoin(Dependent, Employee.id == Dependent.employee_id)
                        .filter(Employee.department_id == department_id)
                        .group_by(Employee.id)
                        .all())
            if not employees: 
                return []  # Retornar lista vazia se não houver colaboradores
            return [{
                'id': emp.Employee.id,
                'name': emp.Employee.name,
                'have_dependents': emp.dependents_count > 0
            } for emp in employees]
        except Exception as e:
            logging.error(f"Erro ao buscar colaboradores do departamento {department_id}: {e}")
            return None  
