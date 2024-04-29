<h1 align="center">API Backend</h1>

Backend da ACMEVita

Projeto de modelagem de dados e criação de uma API utilizando Python e qualquer framework de sua escolha (Flask, FastAPI, Django etc).

<hr/>

# Documentação SWAGGER integrada

![background](https://github.com/TiagoOliverDev/backend_telavita/blob/main/images/image.png)

<hr/>

# Design Patterns utilizado

Basicamente foi usado um tipo de MVC.

- Model representado pelo uso do SQLAlchemy
- Controllers são os endpoints definidos nos Blueprints do Flask, separa em escopos
- Service funcionando como uma ponte entre os Controllers e o Repository
- Repository que funciona como uma abstração do acesso aos dados, que facilita a comunicação com o banco de dados e realiza as querys
- Views retornando dados de requisições em formato JSON


# Padrão de pastas

```
    backend_telavita/
    │
    ├── app/
    │   ├── __init__.py
    │   ├── models/
    │   └── ...
    │   ├── repositories/
    │   └── ...
    │   ├── routes/
    │   └── ...
    │   ├── services/
    │   └── ...
    │   └── swagger/
    │   └── ...
    │
    ├── config/
    │   └── ...
    ├── venv/
    │   └── ...
    ├── images/
    │   └── ...
    ├── migrations/
    │   └── ...
    ├── tests/
    │   └── ...
    │
    ├── .env
    ├── .gitignore
    ├── docker-compose.yml
    ├── Dockerfile
    └── README.md
    ├── requirements.txt
    ├── server.py
 ```

# Features 

# # Departamentos

- Cadastra um novo departamento
- Lista todos os departamentos cadastrados no sistema
- Busca um departamento pelo ID
- Edita um departamento pelo ID
- Exclui um departamento pelo ID


# # Colaboradores

- Cadastra um novo colaborador
- Lista todos os colaboradores de um departamento
- Busca um colaborador pelo ID
- Edita um colaborador pelo ID
- Exclui um colaborador pelo ID


<hr/>

# Tecnologias

Usei as seguintes tecnologias:

- Python >= 3.10.11
- Flask
- SQLAlchemy
- Blueprint
- Unittest
- psycopg2
- Flask-Cors
- Flask-SQLAlchemy
- flask-swagger
- Flask-Testing
- python-dotenv

<hr/>

# Passos para rodar o projeto

## Step 1: Clone o repositório

- Crie uma pasta na sua maquína local e copia o repositório

- Clone [repository](git@github.com:TiagoOliverDev/backend_telavita.git) na sua pasta

  ```
  git clone git@github.com:TiagoOliverDev/backend_telavita.git
  ```

- Navegue até o diretório `cd backend_telavita`

## Step 2: Criar uma env

 python -m venv nome_da_env

 nome_da_env/Scripts/activate

 pip install -r requirements.txt




<hr/>


## Autor

:man: **Tiago Oliveira**

- [GitHub](https://github.com/TiagoOliverDev/)
- [LinkedIn](https://www.linkedin.com/in/tiago-oliveira-49a2a6205/)

## 🤝 Contribua
- Contribuições, issues, e feature são bem vindas!
- Clique aqui para criar uma issue [issues page](https://github.com/TiagoOliverDev/backend_telavita/issues).

# Gostou do projeto ?
Der ⭐ se gostou!
