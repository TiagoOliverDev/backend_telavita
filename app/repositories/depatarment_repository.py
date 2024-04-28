from .db import Db
from sqlalchemy.exc import SQLAlchemyError
from ..models import Department
import logging
import psycopg2

db = Db()

class DepartamentRepository():
    def __init__(self, db):
        self.db = db

    def create_department(self, name: str):
        try:
            new_department = Department(name=name)
            self.db.session.add(new_department)
            self.db.session.commit()
            return new_department.id
        except Exception as e:
            self.db.session.rollback()
            logging.error(f"Erro ao cadastrar o departamento: {e}")
            return None
        
    def exists_department(self, name: str):
        """Verifica se um departamento com o dado nome já existe no banco de dados."""
        return Department.query.filter_by(name=name).first() is not None
        
    def list_departments(self):
        try:
            departments = Department.query.all()
            return departments
        except Exception as e:
            logging.error(f"Erro ao listar departamentos: {e}")
            return []
