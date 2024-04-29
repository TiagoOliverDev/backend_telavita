from flask import Flask, json
import unittest
import sys
import os
import logging
import uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

class EmployeeTestCase(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Setup de testes para colaboradores")
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Inicia uma transação que pode ser revertida depois
        self.transaction = db.session.begin_nested()    
  
                     
    def tearDown(self):
        with self.app_context:
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()
        db.session.remove()
        self.app_context.pop()



    ######## Testes da rota /colaborador/cadastrar ########
    def test_create_employee_success(self):
        """Teste simulando cadastro bem sucedido de colaborador"""

        from app.models import Department
        self.department = Department(name="TI")
        db.session.add(self.department)
        db.session.commit()   

        data = {'name': 'John Doe', 'department_id': self.department.id, 'dependents': ['Jane Doe', 'Baby Doe']}
        response = self.client.post('/colaborador/cadastrar', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('employee_id', response_data)
        self.assertEqual(response_data['message'], 'Colaborador adicionado com sucesso')


    def test_create_employee_duplicate(self):
        """Teste para validar o comportamento quando tenta criar colaborador existente"""

        from app.models import Department, Employee

        self.department = Department(name="TI")
        db.session.add(self.department)
        db.session.commit()   

        employee = Employee(name='Tiago Oliveira', department_id=self.department.id)
        db.session.add(employee)
        db.session.commit()

        data = {'name': 'Tiago Oliveira', 'department_id': self.department.id}
        response = self.client.post('/colaborador/cadastrar', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 409)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['error'], 'Colaborador já existe')



    ######## Testes da rota /colaborador/departamento/<int:department_id>/colaboradores ########
    def test_get_employees_by_department_success(self):
        """Teste para validar se os colaboradores de um determinado departamento são listados"""

        from app.models import Department, Employee
        # Departamento e colaboradores para teste
        self.department = Department(name="Desenvolvimento")
        db.session.add(self.department)
        db.session.commit()

        self.employee1 = Employee(name="Tiago", department_id=self.department.id)
        self.employee2 = Employee(name="Bob", department_id=self.department.id)
        db.session.add_all([self.employee1, self.employee2])
        db.session.commit() 

        response = self.client.get(f'/colaborador/departamento/{self.department.id}/colaboradores')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        self.assertDictContainsSubset({'name': 'Tiago'}, data[0])
        self.assertDictContainsSubset({'name': 'Bob'}, data[1])

    def test_get_employees_by_department_none_found(self):
        """Teste para listar colaboradores de departamento sem colaboradores"""

        from app.models import Department
        empty_department = Department(name="Marketing")
        db.session.add(empty_department)
        db.session.commit()
        
        response = self.client.get(f'/colaborador/departamento/{empty_department.id}/colaboradores')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Nenhum colaborador encontrado')



    ######## Testes da rota /colaborador/editar/<int:employee_id> ########    
    def test_update_employee_success(self):
        """Teste verifica se um colaborador é atualizado corretamente"""

        from app.models import Department, Employee
        self.department = Department(name="Desenvolvimento")
        db.session.add(self.department)
        db.session.commit()

        self.employee = Employee(name="Tiago", department_id=self.department.id)
        db.session.add(self.employee)
        db.session.commit()

        data = {
            'name': 'Tiago Updated',
            'department_id': self.department.id
        }
        
        response = self.client.put(f'/colaborador/editar/{self.employee.id}', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'Colaborador atualizado com sucesso')
        self.assertEqual(response_data['department_id'], self.employee.id)


    def test_update_employee_no_information(self):
        """Teste de atualização de dados do colaborador sem passar nenhum dado"""

        from app.models import Department, Employee
        self.department = Department(name="Desenvolvimento")
        db.session.add(self.department)
        db.session.commit()

        self.employee = Employee(name="Tiago", department_id=self.department.id)
        db.session.add(self.employee)
        db.session.commit()

        data = {}
        response = self.client.put(f'/colaborador/editar/{self.employee.id}', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['error'], 'Nenhuma informação fornecida para atualização')




    ######## Testes da rota /colaborador/excluir/<int:employee_id> ########    
    def test_delete_employee_success(self):
        """Teste para verificar se um colaborador é excluido corretamente"""

        from app.models import Department, Employee
        self.department = Department(name="Desenvolvimento")
        db.session.add(self.department)
        db.session.commit()

        self.employee = Employee(name="Tiago", department_id=self.department.id)
        db.session.add(self.employee)
        db.session.commit()

        response = self.client.delete(f'/colaborador/excluir/{self.employee.id}')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Colaborador excluído com sucesso')
        # Verifique se o colaborador realmente foi removido
        deleted_employee = Employee.query.get(self.employee.id)
        self.assertIsNone(deleted_employee)


    def test_delete_employee_not_found(self):
        """Teste para validar quando se tenta excluir o colaborador com ID inexistente"""

        from app.models import Department, Employee
        self.department = Department(name="Desenvolvimento")
        db.session.add(self.department)
        db.session.commit()

        self.employee = Employee(name="Tiago", department_id=self.department.id)
        db.session.add(self.employee)
        db.session.commit()

        nonexistent_id = self.employee.id + 1000
        response = self.client.delete(f'/colaborador/excluir/{nonexistent_id}')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['error'], 'Colaborador não encontrado')


    ######## Testes da rota /colaborador/busca_por_id/<int:employee_id> ########    
    def test_get_employee_success(self):
        """Teste validando se colaborador com ID válido é retornado corretamente"""

        from app.models import Department, Employee
        self.department = Department(name="Desenvolvimento")
        db.session.add(self.department)
        db.session.commit()

        self.employee = Employee(name="Tiago Oliveira", department_id=self.department.id)
        db.session.add(self.employee)
        db.session.commit()

        response = self.client.get(f'/colaborador/busca_por_id/{self.employee.id}')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['id'], self.employee.id)
        self.assertEqual(response_data['name'], 'Tiago Oliveira')

    def test_get_employee_not_found(self):
        """Teste para quando tenta buscar um colaborador que não existe"""

        from app.models import Department, Employee
        self.department = Department(name="Developers")
        db.session.add(self.department)
        db.session.commit()

        self.employee = Employee(name="Tuco Oliveira", department_id=self.department.id)
        db.session.add(self.employee)
        db.session.commit()

        nonexistent_id = self.employee.id + 1000
        response = self.client.get(f'/colaborador/busca_por_id/{nonexistent_id}')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['error'], 'Colaborador não encontrado')



if __name__ == '__main__':
    unittest.main()