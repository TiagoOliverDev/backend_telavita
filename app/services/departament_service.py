# service.py
from ..repositories import DepartamentRepository
import jwt
import logging


# departament_repository = DepartamentRepository()

class DepartmentService:
    def __init__(self, repository):
        self.repository = repository

    def create_department(self, name: str):
        return self.repository.create_department(name)

    def get_all_departments(self):
        return self.repository.list_departments()
