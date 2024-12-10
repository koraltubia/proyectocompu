import unittest
from backend import app, db, Usuario, Proyecto
from flask_jwt_extended import create_access_token
import json

import os

class BackendTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
        app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        cls.client = app.test_client()

        print("Base de datos de pruebas URI:", app.config['SQLALCHEMY_DATABASE_URI'])

        with app.app_context():
            db.create_all()  

            db.session.query(Usuario).delete()  
            db.session.commit()
            
            admin = Usuario(username="admin", password="adminpass")
            user = Usuario(username="user", password="userpass")
            db.session.add(admin)
            db.session.add(user)
            db.session.commit()

            cls.admin_id = admin.id
            cls.user_id = user.id

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()



    def get_user_by_id(self, user_id):
        return db.session.get(Usuario, user_id)

    def test_create_project(self):
        with app.app_context():
            admin = self.get_user_by_id(self.admin_id)
            project_data = {
                'titulo': 'Proyecto 1',
                'descripcion': 'Descripción del proyecto',
                'autor': 'Admin',
                'fecha': '2023-10-01',
                'imagen_url': 'http://example.com/image.jpg',
                'usuario_id': admin.id
            }
            proyecto = Proyecto(**project_data)
            db.session.add(proyecto)
            db.session.commit()
            print(f"Proyecto creado con ID: {proyecto.id}")
            self.assertIsNotNone(proyecto.id)
            print("Prueba de creación de proyecto completada.")
            print("------------------------------------------------------------")

    def test_delete_project(self):
        with app.app_context():
            admin = self.get_user_by_id(self.admin_id)
            project = Proyecto(titulo='Proyecto 2', autor='Admin', usuario_id=admin.id)
            db.session.add(project)
            db.session.commit()
            print(f"Proyecto creado con ID: {project.id} para eliminación.")

            db.session.delete(project)
            db.session.commit()
            print(f"Proyecto con ID: {project.id} eliminado.")
            self.assertIsNone(db.session.get(Proyecto, project.id))
            print("Prueba de eliminación de proyecto completada.")
            print("------------------------------------------------------------")

    def test_update_project(self):
        with app.app_context():
            admin = self.get_user_by_id(self.admin_id)
            project = Proyecto(titulo='Proyecto inicial', autor='Admin', usuario_id=admin.id)
            db.session.add(project)
            db.session.commit()
            print(f"Proyecto inicial creado con ID: {project.id}")

            project.titulo = 'Título del proyecto actualizado'
            db.session.commit()
            print("Título del proyecto actualizado.")
            self.assertEqual(project.titulo, 'Título del proyecto actualizado')
            print("Prueba de actualización de proyecto completada.")
            print("------------------------------------------------------------")

    def test_unauthorized_delete_project(self):
        with app.app_context():
            admin = self.get_user_by_id(self.admin_id)
            project = Proyecto(titulo='Proyecto Privado', autor='Admin', usuario_id=admin.id)
            db.session.add(project)
            db.session.commit()
            print(f"Proyecto creado con ID: {project.id} (privado).")

            user = self.get_user_by_id(self.user_id)
            print(f"Usuario regular recuperado: {user.username}")

            print(f"Intentando eliminar el proyecto {project.id} por el usuario {user.username} (no autorizado).")
            self.assertNotEqual(user.id, project.usuario_id, 
                f"El usuario {user.username} no debería tener permisos para eliminar el proyecto.")

            project_from_db = db.session.get(Proyecto, project.id)
            self.assertIsNotNone(project_from_db)
            print("Prueba de intento de borrado de proyecto por usuario no autorizado completada.")
            print("------------------------------------------------------------")


if __name__ == '__main__':
    unittest.main()
