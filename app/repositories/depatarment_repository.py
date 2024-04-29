from sqlalchemy.exc import SQLAlchemyError
from ..models import Department
import logging


class DepartamentRepository():
    def __init__(self, db):
        self.db = db

    def create_department(self, name: str):
        """
        Cria um novo departamento no banco de dados.

        Esta função tenta criar um departamento com o nome fornecido. Se a operação
        de inserção no banco de dados for bem-sucedida, ela retorna o ID do novo
        departamento criado. Em caso de falha, faz o rollback da transação e loga o erro.

        Args:
            name (str): O nome do departamento a ser criado.

        Returns:
            int or None: Retorna o ID do departamento criado se bem-sucedido; None se houver falha.
        """
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
        """
        Lista todos os departamentos ordenados pelo ID.

        Esta função recupera todos os departamentos do banco de dados, ordenados pelo
        ID de forma ascendente. Em caso de falha na consulta ao banco, loga o erro e
        retorna uma lista vazia.

        Returns:
            list: Uma lista de objetos Department se a consulta for bem-sucedida,
                ou uma lista vazia se houver falha na consulta.
        """
        try:
            departments = Department.query.order_by(Department.id).all()
            return departments
        except Exception as e:
            logging.error(f"Erro ao listar departamentos: {e}")
            return []
        
    def update_department(self, department_id: int, new_name: str):
        """
        Atualiza o nome de um departamento existente.

        Esta função tenta encontrar um departamento pelo seu ID e atualizar seu nome.
        Se o departamento for encontrado e atualizado com sucesso, retorna True.
        Caso o departamento não seja encontrado ou haja algum erro na transação,
        faz rollback e retorna False.

        Args:
            department_id (int): O ID do departamento a ser atualizado.
            new_name (str): O novo nome a ser atribuído ao departamento.

        Returns:
            bool: True se o departamento for atualizado com sucesso, False caso contrário.
        """
        try:
            department = Department.query.get(department_id)
            if department:
                department.name = new_name
                self.db.session.commit()
                return True
            return False
        except Exception as e:
            self.db.session.rollback()
            logging.error(f"Erro ao atualizar o departamento: {e}")
            return False
        
    def delete_department(self, department_id: int):
        """
        Exclui um departamento específico pelo ID.

        Tenta encontrar e excluir um departamento com base no ID fornecido. Se o departamento
        for encontrado e excluído com sucesso, confirma a transação e retorna True.
        Se o departamento não for encontrado, ou se ocorrer um erro durante a transação,
        realiza rollback e retorna False.

        Args:
            department_id (int): O ID do departamento a ser excluído.

        Returns:
            bool: True se o departamento for excluído com sucesso, False caso contrário.
        """
        try:
            department = Department.query.get(department_id)
            if department:
                self.db.session.delete(department)
                self.db.session.commit()
                return True
            return False
        except Exception as e:
            self.db.session.rollback()
            logging.error(f"Erro ao excluir o departamento: {e}")
            return False
        
    def get_department_by_id(self, department_id: int):
        """
        Busca um departamento pelo seu ID.

        Realiza uma consulta ao banco de dados para encontrar um departamento pelo ID especificado.
        Retorna o objeto Department se encontrado, ou None se não houver departamento com o ID fornecido.

        Args:
            department_id (int): O ID do departamento a ser buscado.

        Returns:
            Department or None: O objeto Department se encontrado, None se não houver departamento correspondente.
        """
        try:
            department = Department.query.get(department_id)
            if department:
                return department
            else:
                return None
        except Exception as e:
            logging.error(f"Erro ao buscar o departamento: {e}")
            return None
