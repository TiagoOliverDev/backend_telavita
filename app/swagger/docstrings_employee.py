class EmployeeDocstrings:
    """Documentation for endpoints."""
    
    create_employee =     """
    Cadastra um novo colaborador no sistema.
    ---
    tags:
      - Colaboradores
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - department_id
          properties:
            name:
              type: string
              description: Nome completo do colaborador.
            department_id:
              type: integer
              description: ID do departamento ao qual o colaborador será associado.
            dependents:
              type: array
              items:
                type: string
              description: Lista de nomes de dependentes do colaborador (opcional).
    responses:
      201:
        description: Colaborador cadastrado com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Colaborador adicionado com sucesso.
            employee_id:
              type: integer
              example: 1
      400:
        description: Informação necessária não fornecida ou inválida.
        schema:
          type: object
          properties:
            error:
              type: string
              example: Nome e departamento são obrigatórios.
      409:
        description: Colaborador com o mesmo nome já existe.
        schema:
          type: object
          properties:
            error:
              type: string
              example: Colaborador já existe.
      500:
        description: Erro interno do servidor.
        schema:
          type: object
          properties:
            error:
              type: string
              example: Erro interno no servidor ao tentar adicionar colaborador.
    """

    get_employees_by_department = """
    Lista todos os colaboradores de um departamento específico.
    ---
    tags:
      - Colaboradores
    parameters:
      - in: path
        name: department_id
        type: integer
        required: true
        description: Identificador único do departamento do qual os colaboradores serão listados.
    responses:
      200:
        description: Lista de colaboradores encontrada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: Identificador único do colaborador.
                example: 101
              name:
                type: string
                description: Nome do colaborador.
                example: "João Silva"
              department_id:
                type: integer
                description: Identificador do departamento ao qual o colaborador pertence.
                example: 1
      404:
        description: Nenhum colaborador encontrado no departamento especificado.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Nenhum colaborador encontrado"
      500:
        description: Erro ao acessar o banco de dados ou erro interno no servidor.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao acessar o banco de dados"
    """

    update_employee =  """
    Atualiza informações de um colaborador existente.
    ---
    tags:
      - Colaboradores
    consumes:
      - application/json
    parameters:
      - name: employee_id
        in: path
        type: integer
        required: true
        description: Identificador único do colaborador.
      - name: body
        in: body
        required: false
        schema:
          type: object
          properties:
            name:
              type: string
              description: Novo nome do colaborador.
            department_id:
              type: integer
              description: Novo ID do departamento ao qual o colaborador será realocado.
            dependents:
              type: array
              items:
                type: string
              description: Lista atualizada de nomes de dependentes.
    responses:
      200:
        description: Colaborador atualizado com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
              example: 'Colaborador atualizado com sucesso.'
            department_id:
              type: integer
              example: 5
      400:
        description: Nenhuma informação fornecida para atualização.
        schema:
          type: object
          properties:
            error:
              type: string
              example: 'Nenhuma informação fornecida para atualização.'
      409:
        description: Nome de colaborador já existe.
        schema:
          type: object
          properties:
            error:
              type: string
              example: 'Nome de colaborador já existe.'
      500:
        description: Erro interno ao tentar atualizar o colaborador.
        schema:
          type: object
          properties:
            error:
              type: string
              example: 'Erro interno no servidor ao tentar atualizar colaborador.'
    """

    delete_department = """
    Exclui um colaborador pelo seu identificador único.
    ---
    tags:
      - Colaboradores
    parameters:
      - in: path
        name: employee_id
        type: integer
        required: true
        description: Identificador único do colaborador que será excluído.
    responses:
      200:
        description: Colaborador excluído com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
              example: 'Colaborador excluído com sucesso.'
      404:
        description: Colaborador não encontrado.
        schema:
          type: object
          properties:
            error:
              type: string
              example: 'Colaborador não encontrado.'
      500:
        description: Erro interno ao tentar excluir o colaborador.
        schema:
          type: object
          properties:
            error:
              type: string
              example: 'Erro interno no servidor ao tentar excluir colaborador.'
    """

    get_department =  """
    Busca um colaborador pelo seu identificador único.
    ---
    tags:
      - Colaboradores
    parameters:
      - in: path
        name: employee_id
        type: integer
        required: true
        description: Identificador único do colaborador a ser consultado.
    responses:
      200:
        description: Detalhes do colaborador encontrado com sucesso.
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 101
            name:
              type: string
              example: "João Silva"
            department_id:
              type: integer
              example: 5
            dependents:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: "Maria Silva"
      404:
        description: Colaborador não encontrado.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "employee não encontrado"
      500:
        description: Erro interno ao processar a solicitação.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro interno do servidor"
    """



