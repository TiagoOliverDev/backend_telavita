from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from ..models import Employee, Dependent
from sqlalchemy.orm import joinedload
import logging


class EmployeeRepository():
    def __init__(self, db):
        self.db = db

    def create_employee(self, name: str, department_id: int, dependents=None):
        """
        Adiciona um novo colaborador ao banco de dados e, opcionalmente, seus dependentes.

        Esta função cria um novo colaborador com o nome e o ID do departamento fornecidos.
        Se houver dependentes, eles também serão adicionados ao banco de dados. A função
        tenta salvar todas as informações no banco de dados e, se bem-sucedida, retorna o ID
        do novo colaborador. Se ocorrer uma falha durante a transação, realiza um rollback.

        Args:
            name (str): O nome do colaborador.
            department_id (int): O ID do departamento ao qual o colaborador pertencerá.
            dependents (list of str, optional): Uma lista de nomes de dependentes do colaborador.

        Returns:
            int or None: Retorna o ID do novo colaborador se bem-sucedido; None em caso de falha.
        """
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
        """
        Retorna uma lista de colaboradores de um determinado departamento, indicando se têm dependentes.

        Busca no banco de dados todos os colaboradores de um departamento específico, junto com a contagem
        de seus dependentes. Retorna uma lista de dicionários com detalhes dos colaboradores e uma flag 
        booleana indicando a presença de dependentes.

        Args:
            department_id (int): ID do departamento do qual se deseja listar colaboradores.

        Returns:
            list of dict: Uma lista contendo dicionários com informações dos colaboradores e uma flag 
                        'have_dependents' para indicar se possuem dependentes. Retorna uma lista vazia
                        se nenhum colaborador for encontrado.
        """
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
        """
        Atualiza os dados de um colaborador existente no banco de dados.

        Esta função permite atualizar o nome, o departamento e/ou os dependentes de um colaborador específico.
        Se algum dos parâmetros é fornecido, a função aplica as alterações correspondentes. A atualização dos
        dependentes envolve remover todos os dependentes atuais e adicionar os novos fornecidos na lista.

        Args:
            employee_id (int): O ID do colaborador cujos dados serão atualizados.
            new_name (str, optional): O novo nome do colaborador, se uma alteração for necessária.
            new_department_id (int, optional): O novo ID do departamento, se uma mudança for necessária.
            new_dependents (list of str, optional): Uma nova lista de nomes de dependentes para substituir
                                                    os atuais, se uma mudança for necessária.

        Returns:
            bool: True se a atualização for bem-sucedida, False se falhar devido a um erro ou se o colaborador
                não for encontrado.

        Raises:
            Exception: Captura e loga qualquer exceção que ocorra durante a operação de atualização,
                    realizando rollback na transação para manter a integridade dos dados.
        """
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
        """
        Exclui um colaborador existente do banco de dados.

        Busca o colaborador pelo ID fornecido e, se encontrado, remove-o do banco de dados. Se a operação
        de exclusão for bem-sucedida, confirma a transação e retorna True. Se o colaborador não for encontrado,
        ou se ocorrer algum erro durante a exclusão, a função retorna False.

        Args:
            employee_id (int): O ID do colaborador a ser excluído.

        Returns:
            bool: True se o colaborador for excluído com sucesso, False caso contrário.

        Raises:
            Exception: Loga e retorna False em caso de qualquer exceção, garantindo que nenhum dado parcial seja salvo.
        """
        try:
            employee = Employee.query.get(employee_id)
            if employee:
                self.db.session.delete(employee)
                self.db.session.commit()
                return True
            return False
        except Exception as e:
            self.db.session.rollback()
            logging.error(f"Erro ao excluir o colaborador: {e}")
            return False
        
    def get_employee_by_id(self, employee_id: int):
        """
        Recupera um colaborador pelo seu ID, incluindo informações sobre seu departamento e dependentes.

        A função busca no banco de dados o colaborador especificado pelo ID, incluindo detalhes de seus dependentes
        e o departamento ao qual pertence. Retorna um dicionário com os dados do colaborador se encontrado.
        Retorna None se o colaborador não for encontrado ou em caso de erro na consulta.

        Args:
            employee_id (int): O ID do colaborador a ser buscado.

        Returns:
            dict or None: Um dicionário contendo informações do colaborador, seu departamento e dependentes, ou None
                        se não for encontrado ou em caso de erro.

        Raises:
            Exception: Loga um erro se ocorrer uma exceção durante a busca.
        """
        try:
            employee = (Employee.query
                        .options(joinedload(Employee.department), joinedload(Employee.dependents))
                        .get(employee_id))
            if not employee:
                return None

            return {
                'id': employee.id,
                'name': employee.name,
                'department': {
                    'id': employee.department.id,
                    'name': employee.department.name
                },
                'dependents': [{'id': dependent.id, 'name': dependent.name} for dependent in employee.dependents]
            }
        except Exception as e:
            logging.error(f"Erro ao buscar o colaborador: {e}")
            return None
            

