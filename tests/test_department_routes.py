import unittest
from flask import Flask, json
import sys
import os
import logging
import uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

class DepartmentTestCase(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Setting up test case")
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        logging.debug("Application context pushed")

        # Limpa o banco de dados antes do teste
        db.create_all()

        # Inicia uma transação que pode ser revertida depois
        self.transaction = db.session.begin_nested()
        
                
    def tearDown(self):
        with self.app_context:
            # Limpa todas as tabelas manualmente
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()
        db.session.remove()
        self.app_context.pop()
        
    def test_create_department(self):
        # Dados para o teste com nome dinâmico
        unique_name = f'Desenvolvimento-{uuid.uuid4()}'
        data = {'name': unique_name}
        response = self.client.post('/departament/cadastrar', data=json.dumps(data), content_type='application/json')
        
        # Verifica se o departamento foi criado
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('department_id', response_data.keys())
        self.assertEqual(response_data['message'], 'Departamento criado com sucesso')


    def test_create_department_without_name(self):
        # Testar a criação de departamento sem fornecer o nome
        data = {}
        response = self.client.post('/departament/cadastrar', data=json.dumps(data), content_type='application/json')
        
        # Verifica se o erro correto é retornado
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.data).keys())
        self.assertEqual(json.loads(response.data)['error'], 'O nome do departamento é obrigatório')
    

    def test_list_departments_success(self):
        # Preparando dados de teste
        from app.models import Department
        dep1 = Department(name=f"HR")
        dep2 = Department(name=f"Development")
        with self.app.app_context():
            db.session.add(dep1)
            db.session.add(dep2)
            db.session.commit()
        
        # Teste GET request
        response = self.client.get('/departament/listar')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], f"HR")
        self.assertEqual(data[1]['name'], f"Development")
    

    def test_list_departments_failure(self):
        # Simulando uma falha através do patching
        from app.services.departament_service import DepartmentService
        from unittest.mock import patch
        with patch.object(DepartmentService, 'get_all_departments', side_effect=Exception('Database error')):
            response = self.client.get('/departament/listar')
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Database error')







if __name__ == '__main__':
    unittest.main()