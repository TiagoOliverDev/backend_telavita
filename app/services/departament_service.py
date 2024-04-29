import logging

class DepartmentService:
    def __init__(self, repository):
        self.repository = repository

    def create_department(self, name: str):
        """
        Cria um novo departamento se ele ainda não existir.

        Verifica se já existe um departamento com o nome fornecido. Se existir, retorna uma mensagem indicando
        que já existe. Se não, tenta criar um novo departamento e retorna uma mensagem de sucesso ou de falha.

        Args:
            name (str): Nome do departamento a ser criado.

        Returns:
            tuple: (None, message) se o departamento já existe ou falha ao criar;
                (department_id, message) se criado com sucesso.
        """
        if self.repository.exists_department(name):
            return None, 'Departamento já existe'
        
        try:
            department_id = self.repository.create_department(name)
            if department_id:
                return department_id, 'Departamento criado com sucesso'
            else:
                return None, 'Falha ao criar departamento. O departamento já existe!'
        except Exception as e:
            logging.error(f"Erro ao cadastrar departamento: {e}")
            return None
        
    def get_all_departments(self):
        """
        Lista todos os departamentos existentes.

        Tenta recuperar e retornar todos os departamentos do banco de dados. Em caso de falha, retorna None.

        Returns:
            list or None: Lista dos departamentos se bem-sucedido, None em caso de falha.
        """
        try:
            departments = self.repository.list_departments()
            return departments
        except Exception as e:
            logging.error(f"Erro ao listar departamentos: {e}")
            return None

    def update_department(self, department_id: int, new_name: str):
        """
        Atualiza o nome de um departamento existente.

        Verifica se o novo nome já existe. Se sim, retorna um erro. Se não, tenta atualizar o departamento
        com o novo nome e retorna uma mensagem de sucesso ou falha.

        Args:
            department_id (int): ID do departamento a ser atualizado.
            new_name (str): Novo nome para o departamento.

        Returns:
            tuple: (None, message) se o nome já existe ou falha na atualização;
                (department_id, message) se atualizado com sucesso.
        """
        if self.repository.exists_department(new_name):
            return None, 'Nome de departamento já existe'
        
        try:
            if self.repository.update_department(department_id, new_name):
                return department_id, 'Departamento atualizado com sucesso'
            else:
                return 'Erro ao atualizar departamento ou departamento não encontrado', False
        except Exception as e:
            logging.error(f"Erro ao editar departamento: {e}")
            return None

    def delete_department(self, department_id: int):
        """
        Exclui um departamento existente.

        Verifica primeiro se o departamento existe. Se não, retorna um erro. Se sim, tenta excluir
        e retorna uma mensagem de sucesso ou de falha.

        Args:
            department_id (int): ID do departamento a ser excluído.

        Returns:
            tuple: (message, success) indicando o resultado da operação.
        """
        try:
            department = self.repository.get_department_by_id(department_id)
            if not department:
                return 'Departamento não encontrado', False

            if self.repository.delete_department(department_id):
                return 'Departamento excluído com sucesso', True
            else:
                return 'Erro ao excluir o departamento', False
        except Exception as e:
            logging.error(f"Erro ao tentar excluir o departamento: {e}")
            return 'Erro interno ao tentar excluir o departamento', False
           
    def get_department_by_id(self, department_id: int):
        """
        Busca um departamento pelo seu ID.

        Tenta encontrar e retornar o departamento especificado pelo ID. Se encontrado, retorna os dados do departamento;
        se não, retorna um erro.

        Args:
            department_id (int): ID do departamento a ser buscado.

        Returns:
            tuple: ({'id': id, 'name': name}, success) se encontrado;
                (message, success) se não encontrado ou erro.
        """
        try:
            department = self.repository.get_department_by_id(department_id)
            if department:
                return {'id': department.id, 'name': department.name}, True
            else:
                return 'Departamento não encontrado', False
        except Exception as e:
            logging.error(f"Erro ao buscar o departamento por ID: {e}")
            return 'Erro interno ao buscar o departamento', False