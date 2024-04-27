class ProductionConfig:
    DEBUG = False
    SECRET_KEY = '9ba263503b01ce2ef81f6641f504b45333aa0662183d0184db79d9e92ccef620'
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@hostname/production_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
