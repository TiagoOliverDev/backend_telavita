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
    ├── migrate.py
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
- PostgreSQL 
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

# # windows

 python -m venv nome_da_env

 nome_da_env/Scripts/activate

 pip install -r requirements.txt


# # Linux

 python3 -m venv meu_venv

 source meu_venv/bin/activate

 pip install -r requirements.txt


## Step 3: Criar dois bancos (teste, desenvolvimento) local no Postgresql (PgAdmin 4, Dbeaver, etc..)

  O de teste deve se chamar:

  ```
  testing_db
  ```

  O de desenvolvimento deve se chamar:

  ```
  teste10
  ```

## Step 4: Criar migrations 

  Rode o migrate.py para realizar as migrations (certifique-se de não ter nenhuma pasta /migrations na raiz do projeto)

  ```
  python migrate.py
  ```


## Step 5: Rodar API e ativar Swagger doc

  Abra dois terminals/CMD

  Em um rode o comando para startar a API:

  ```
  python server.py
  ```

  No outro rode o comando para ativar o docker da Swagger doc:


  ```
  docker run -p 80:8080 -e URL=http://localhost:1010/swagger swaggerapi/swagger-ui
  ```

# Agora pode acessar os links abaixo e testar a API via interface Swagger

  - Dica: começar a testar pelos endpoints de cadastro (department/cadastro e colaborador/cadastro)

  ```
  http://localhost/
  ```

  ```
  http://localhost:1010/swagger
  ```

<hr/>

## AINDA NÃO ACABOU! Tem os testes unitários básicos!

  - Vá até .env e comente a variavel FLASK_ENV=development e descomente a FLASK_ENV=testing Com isso o ambiente será totalmente de testes!
  - Agora é só rodar os testes, que no total são 22 testes básicos de endpoints
  - Fiz entre dois a três testes por endpoint usando Unitest

  Rode com:

  ```
  python .\tests\test_department_routes.py
  ```

  ```
  python .\tests\test_employee_routes.py
  ```

## OBS:

   - Criei o projeto todo adaptado para rodar com "docker-compose up" startando as imagens docker (API e Swagger) e roda normalmente mas infelizmente dá alguns conflito com o PostgreSql que mesmo permitindo conexões remota ele não conecta por conta do uso do SqlAlchemy dai acaba que não fica sendo possível testar a Api swagger dessa forma pelo docker-compose, por isso deixei mais manual a forma de rodar o projeto acima, aonde starto apenas o docker do Swagger e rodo a API manualmente, com isso fica mais fácil de testar.

## Autor

:man: **Tiago Oliveira**

- [GitHub](https://github.com/TiagoOliverDev/)
- [LinkedIn](https://www.linkedin.com/in/tiago-oliveira-49a2a6205/)

## 🤝 Contribua
- Contribuições, issues, e feature são bem vindas!
- Clique aqui para criar uma issue [issues page](https://github.com/TiagoOliverDev/backend_telavita/issues).

# Gostou do projeto ?
Der ⭐ se gostou!
