import logging

class EmployeeService:
    def __init__(self, repository):
        self.repository = repository

    def create_employee(self, name: str, department_id: int, dependents=None):
        """
        Adiciona um novo colaborador ao banco de dados, juntamente com seus dependentes, se fornecidos.

        Verifica primeiro se já existe um colaborador com o mesmo nome. Se existir, retorna uma mensagem de erro.
        Se não, tenta adicionar o novo colaborador e seus dependentes ao banco de dados. Retorna o ID do novo
        colaborador e uma mensagem de sucesso se a adição for bem-sucedida, ou None em caso de falha.

        Args:
            name (str): Nome do colaborador a ser adicionado.
            department_id (int): ID do departamento ao qual o colaborador pertence.
            dependents (list of str, optional): Lista opcional de nomes dos dependentes do colaborador.

        Returns:
            tuple: (None, message) se o colaborador já existir ou falhar ao adicionar;
                (employee_id, message) se adicionado com sucesso.
        """
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
        """
        Busca todos os colaboradores de um departamento específico.

        Tenta recuperar uma lista de colaboradores de um departamento pelo ID fornecido. Se bem-sucedido,
        retorna a lista de colaboradores; se não houver colaboradores ou ocorrer um erro, retorna None.

        Args:
            department_id (int): ID do departamento do qual os colaboradores serão listados.

        Returns:
            list or None: Lista dos colaboradores se bem-sucedido, None em caso de falha.
        """
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
        """
        Atualiza os dados de um colaborador existente.

        Verifica a existência de um nome duplicado antes de atualizar o colaborador. Se o nome não existir, procede
        com a atualização de nome, departamento e dependentes conforme fornecido. Retorna o ID do colaborador e uma
        mensagem de sucesso se a atualização for bem-sucedida, ou uma mensagem de erro caso contrário.

        Args:
            employee_id (int): ID do colaborador a ser atualizado.
            new_name (str, optional): Novo nome do colaborador.
            new_department_id (int, optional): Novo ID de departamento do colaborador.
            new_dependents (list of str, optional): Nova lista de dependentes do colaborador.

        Returns:
            tuple: (None, message) se ocorrer um erro ou se o nome já existir;
                (employee_id, message) se atualizado com sucesso.
        """
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
        """
        Exclui um colaborador do sistema.

        Verifica primeiro se o colaborador existe. Se existir, tenta excluí-lo e retorna uma mensagem de sucesso.
        Se não existir ou ocorrer um erro durante a exclusão, retorna uma mensagem de erro.

        Args:
            employee_id (int): ID do colaborador a ser excluído.

        Returns:
            tuple: (message, success) indicando o resultado da operação.
        """
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
        """
        Busca um colaborador pelo seu ID.

        Tenta encontrar e retornar os detalhes de um colaborador pelo ID fornecido. Se o colaborador for encontrado,
        retorna seus detalhes; se não, retorna uma mensagem de erro.

        Args:
            employee_id (int): ID do colaborador a ser buscado.

        Returns:
            tuple: (employee_data, success) se encontrado;
                (message, success) se não encontrado ou erro.
        """
        try:
            employee_data = self.repository.get_employee_by_id(employee_id)
            if employee_data:
                return employee_data, True
            else:
                return 'Colaborador não encontrado', False
        except Exception as e:
            logging.error(f"Erro ao buscar o colaborador por ID: {e}")
            return 'Erro interno ao buscar o colaborador', False
        

