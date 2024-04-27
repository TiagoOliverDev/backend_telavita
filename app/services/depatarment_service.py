# service.py
from passlib.hash import bcrypt
from ..repositories.departament_repository import DepartamentRepository
import jwt
import logging


departament_repository = DepartamentRepository()

class DepartamentService:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        
    def list_all_departaments(self):
        try:
            departaments = departament_repository.list_all_departaments()
            if departaments is None:
                return None, 'Error fetching departaments'
            return departaments, None
        except Exception as e:
            logging.error(f"Error fetching departaments: {e}")
            return None, 'Internal server error'

    def format_departaments_all(self, departaments):
        formatted_departaments = []
        for departament in departaments:
            formatted_departament = {
                "id": departament[0],
                "nomeSetor": departament[1],
                "created_at": departament[2].strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "updated_at": departament[3].strftime("%a, %d %b %Y %H:%M:%S GMT")
            }
            formatted_departaments.append(formatted_departament)
        return formatted_departaments
        
    def register_departament(self, name: str):
        try:
            if departament_repository.departament_exists(name=name):
                return None, 'departament already exists'

            departament_created = departament_repository.departament_create(name=name)
            return departament_created, None
        except Exception as e:
            logging.error(f"Error registering departament: {e}")
            return None, 'Error registering departament. Please try again later.'
    
    def list_departament_by_id(self, id: int):
        try:
            departament, error = departament_repository.list_departament_by_id(id=id)
            return departament, None
        except Exception as e:
            logging.error(f"Error list departament: {e}")
            return None, 'Error list departament. Please try again later.'
    
    def update_departament(self, id: int, name: str):
        try:
            departament_edited = departament_repository.update_departament(id=id, new_name=name)
            return departament_edited, None
        except Exception as e:
            logging.error(f"Error edit departament: {e}")
            return None, 'Error edit departament. Please try again later.'
        
    def departament_delete(self, id: int):
        try:
            departament_excluded = departament_repository.departament_delete(id=id)
            return departament_excluded, None
        except Exception as e:
            logging.error(f"Error in excluded departament: {e}")
            return None, 'Error in excluded departament. Please try again later.'

    def set_departament(self, id_setor: int, id_usuario: int):
        try:
            set_journey = departament_repository.set_departament(id_setor=id_setor, id_usuario=id_usuario)
            return set_journey, None
        except Exception as e:
            logging.error(f"Error in set journey: {e}")
            return None, 'Error in set journey. Please try again later.'