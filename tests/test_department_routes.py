from flask import Flask, json
import unittest
import sys
import os
import logging
import uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

class DepartmentTestCase(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Setup de testes")
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
        

    ######## Testes da rota /departament/cadastrar ########
    def test_create_department(self):
        """Testa a criação de um novo departamento"""

        unique_name = f'Desenvolvimento-{uuid.uuid4()}'
        data = {'name': unique_name}
        response = self.client.post('/departament/cadastrar', data=json.dumps(data), content_type='application/json')
        
        # Verifica se o departamento foi criado
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('department_id', response_data.keys())
        self.assertEqual(response_data['message'], 'Departamento criado com sucesso')

    def test_create_department_without_name(self):
        """Testar a criação de departamento sem fornecer o nome"""

        data = {}
        response = self.client.post('/departament/cadastrar', data=json.dumps(data), content_type='application/json')
        
        # Verifica se o erro correto é retornado
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.data).keys())
        self.assertEqual(json.loads(response.data)['error'], 'O nome do departamento é obrigatório')

    def test_create_department_with_existing_name(self):
        """Testa a tentativa de criar um departamento com um nome que já existe."""
        
        from app.models import Department
        existing_name = "Financeiro"
        department = Department(name=existing_name)
        db.session.add(department)
        db.session.commit()
        
        data = {'name': existing_name}
        response = self.client.post('/departament/cadastrar', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 409)  
        response_data = json.loads(response.data)
        self.assertIn('error', response_data.keys())
        self.assertEqual(response_data['error'], 'Departamento já existe')


    ######## Testes da rota /departament/listar ########
    def test_list_departments_success(self):
        """Adiciona dois novos departamentos e valida se os dois foram adicionados e se estão sendo retornados na ordem correta"""

        from app.models import Department
        dep1 = Department(name=f"HR")
        dep2 = Department(name=f"Development")
        with self.app.app_context():
            db.session.add(dep1)
            db.session.add(dep2)
            db.session.commit()
        
        response = self.client.get('/departament/listar')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], f"HR")
        self.assertEqual(data[1]['name'], f"Development")
    
    def test_list_departments_failure(self):
        """Simulando uma falha através do patching"""

        from app.services.departament_service import DepartmentService
        from unittest.mock import patch
        with patch.object(DepartmentService, 'get_all_departments', side_effect=Exception('Database error')):
            response = self.client.get('/departament/listar')
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Database error')

    
    ######## Testes da rota /departament//editar/<int:department_id>########
    def test_update_department_success(self):
        """Teste de atualização bem-sucedida"""

        # Primeiro crio um departamento para depois editar
        from app.models import Department
        self.department = Department(name="Original")
        db.session.add(self.department)
        db.session.commit()

        response = self.client.put(
            f'/departament/editar/{self.department.id}',
            data=json.dumps({'name': 'Updated'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Departamento atualizado com sucesso')
        self.assertEqual(data['department_id'], self.department.id)

    def test_update_department_without_name(self):
        """Teste falha ao tentar atualizar sem fornecer um novo nome"""

        from app.models import Department
        self.department = Department(name="Original")
        db.session.add(self.department)
        db.session.commit()

        response = self.client.put(
            f'/departament/editar/{self.department.id}',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'O novo nome do departamento é obrigatório')

    def test_update_department_name_exists(self):
        """Teste falha devido ao nome do departamento já existente"""

        from app.models import Department
        self.department = Department(name="Original")
        db.session.add(self.department)
        db.session.commit()
    
        new_department = Department(name="Existing")
        db.session.add(new_department)
        db.session.commit()
        response = self.client.put(
            f'/departament/editar/{self.department.id}',
            data=json.dumps({'name': 'Existing'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Nome de departamento já existe')



    ######## Testes da rota /departament/excluir/<int:department_id>########
    def test_delete_department_success(self):
        """Testa a exclusão de um departamento"""

        from app.models import Department
        self.department = Department(name="Original")
        db.session.add(self.department)
        db.session.commit()

        response = self.client.delete(f'/departament/excluir/{self.department.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Departamento excluído com sucesso')
        
        # Verificar se o departamento realmente foi removido
        department = Department.query.get(self.department.id)
        self.assertIsNone(department)

    def test_delete_department_not_found(self):
        """Teste usando um ID que não existe para excluir"""

        from app.models import Department
        self.department = Department(name="Original")
        db.session.add(self.department)
        db.session.commit()

        nonexistent_id = self.department.id + 1000
        response = self.client.delete(f'/departament/excluir/{nonexistent_id}')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Departamento não encontrado')



    ######## Testes da rota /departament/busca_por_id/<int:department_id>########
    def test_get_department_success(self):
        """Teste para validar se um DP é retornado corretamente com um ID válido"""

        from app.models import Department
        self.department = Department(name="HR")
        db.session.add(self.department)
        db.session.commit()

        response = self.client.get(f'/departament/busca_por_id/{self.department.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], self.department.id)
        self.assertEqual(data['name'], 'HR')


    def test_get_department_not_found(self):
        """Teste usando um ID que não existe"""

        from app.models import Department
        self.department = Department(name="HR")
        db.session.add(self.department)
        db.session.commit()

        nonexistent_id = self.department.id + 1000
        response = self.client.get(f'/departament/busca_por_id/{nonexistent_id}')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Departamento não encontrado')






if __name__ == '__main__':
    unittest.main()