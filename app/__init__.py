from flask import Flask, jsonify
from flask_migrate import Migrate
from app.models import db, Department, Employee, Dependent  
from app.routes import routes_blueprint
from config import DevelopmentConfig, ProductionConfig, TestingConfig
from flask_swagger import swagger
from flask_cors import CORS, cross_origin
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    if os.environ.get('FLASK_ENV') == 'production':
        env_config = ProductionConfig
    elif os.environ.get('FLASK_ENV') == 'test':
        env_config = TestingConfig
    else:
        env_config = DevelopmentConfig

    app.config.from_object(env_config)
    db.init_app(app)

    migrate = Migrate(app, db)
    
    app.register_blueprint(routes_blueprint)

    # Configuração do Swagger
    @app.route('/swagger')
    @cross_origin()
    def swagger_api():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "ACME API"
        return jsonify(swag)

    return app
