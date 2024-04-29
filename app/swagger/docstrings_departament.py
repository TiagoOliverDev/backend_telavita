class DepartmentDocstrings:
    """Documentation for endpoints."""
    
    create_department = """
    Cadastra um novo departamento no sistema.
    ---
    tags:
      - Departamentos
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              description: Nome do departamento a ser criado.
    responses:
      201:
        description: Departamento criado com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Departamento criado com sucesso.
            department_id:
              type: integer
              example: 1
      400:
        description: Informação necessária não fornecida ou inválida.
        schema:
          type: object
          properties:
            error:
              type: string
              example: O nome do departamento é obrigatório.
      409:
        description: Conflito com um departamento existente.
        schema:
          type: object
          properties:
            error:
              type: string
              example: Departamento já existe.
      500:
        description: Erro interno do servidor ao tentar criar o departamento.
        schema:
          type: object
          properties:
            error:
              type: string
              example: Erro ao tentar criar o departamento.
    """

    list_departments =  """
    Lista todos os departamentos cadastrados no sistema.
    ---
    tags:
      - Departamentos
    responses:
      200:
        description: Uma lista de todos os departamentos cadastrados.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: O identificador único do departamento.
                example: 1
              name:
                type: string
                description: O nome do departamento.
                example: "Recursos Humanos"
      500:
        description: Erro ao recuperar os departamentos do banco de dados.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao recuperar departamentos!"
    """

    update_departments =  """
    Atualiza os dados de um departamento existente.
    ---
    tags:
      - Departamentos
    consumes:
      - application/json
    parameters:
      - in: path
        name: department_id
        type: integer
        required: true
        description: Identificador único do departamento.
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: Novo nome do departamento.
              required: true
    responses:
      200:
        description: Nome do departamento atualizado com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Departamento atualizado com sucesso.
            department_id:
              type: integer
              example: 1
      400:
        description: Falha na validação do pedido.
        schema:
          type: object
          properties:
            error:
              type: string
              example: O novo nome do departamento é obrigatório.
      409:
        description: Conflito por nome de departamento já existente.
        schema:
          type: object
          properties:
            error:
              type: string
              example: Nome de departamento já existe.
      500:
        description: Erro interno ao tentar atualizar o departamento.
        schema:
          type: object
          properties:
            error:
              type: string
              example: Erro ao tentar atualizar o departamento.
    """

    delete_department = """
    Exclui um departamento específico pelo seu ID.
    ---
    tags:
      - Departamentos
    parameters:
      - in: path
        name: department_id
        type: integer
        required: true
        description: Identificador único do departamento a ser excluído.
    responses:
      200:
        description: Departamento excluído com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Departamento excluído com sucesso.
      404:
        description: Departamento não encontrado.
        schema:
          type: object
          properties:
            error:
              type: string
              example: Departamento não encontrado.
      500:
        description: Erro interno ao excluir o departamento.
        schema:
          type: object
          properties:
            error:
              type: string
              example: Erro ao tentar excluir o departamento.
    """

    get_department_by_id = """
    Busca um departamento pelo seu identificador único.
    ---
    tags:
      - Departamentos
    parameters:
      - in: path
        name: department_id
        type: integer
        required: true
        description: Identificador único do departamento.
    responses:
      200:
        description: Departamento encontrado com sucesso.
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "Recursos Humanos"
      404:
        description: Departamento não encontrado.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Departamento não encontrado"
      500:
        description: Erro interno ao processar a solicitação.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro interno do servidor"
    """
