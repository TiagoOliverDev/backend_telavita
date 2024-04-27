from . import db

class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employees = db.relationship('Employee', backref='department', lazy=True)

class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    dependents = db.relationship('Dependent', backref='employee', lazy=True)

class Dependent(db.Model):
    __tablename__ = "dependent"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)



