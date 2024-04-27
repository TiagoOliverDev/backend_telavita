from flask import Flask
from flask_migrate import Migrate
from app.models import db, Department, Employee, Dependent  
from app.routes import routes_blueprint
from config import DevelopmentConfig, ProductionConfig, TestingConfig
import os

def create_app():
    app = Flask(__name__)

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

    return app
