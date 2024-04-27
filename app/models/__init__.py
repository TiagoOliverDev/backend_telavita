from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .models import Department, Employee, Dependent