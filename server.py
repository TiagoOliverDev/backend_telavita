from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from app.routes import routes_blueprint
from flask_cors import CORS
from config import DevelopmentConfig, ProductionConfig
import logging
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    if os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
        logging.info('PRODUÇÃO')
    elif os.environ.get('FLASK_ENV') == 'development':
        app.config.from_object(DevelopmentConfig)
        logging.info('DESENVOLVIMENTO')
    else:
        app.config.from_object(DevelopmentConfig)
        logging.info('TESTE')


    db.init_app(app)

    bcrypt = Bcrypt(app)
    app.register_blueprint(routes_blueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=app.config['DEBUG'])