class DevelopmentConfig:
    DEBUG = True
    # lembrar de alocar a secret key no .env
    SECRET_KEY = '9ba263503b01ce2ef81f6641f504b45333aa0662183d0184db79d9e92ccef620'
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/development_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
