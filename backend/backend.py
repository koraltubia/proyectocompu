
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

#para comprobar que la api funciona
@app.route('/')
def home():
    return {'message': 'API is working'}

@app.route('/api/test')
def test():
    return {'message': 'Test endpoint working'}

# Configuración de la base de datos
DB_NAME = 'proyects.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    proyectos = db.relationship('Proyecto', backref='usuario', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.String(100), nullable=True)
    descripcion = db.Column(db.String(500), nullable=True)
    imagen_url = db.Column(db.String(255), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

def init_db():

    if not os.path.exists(DB_NAME):
        with app.app_context():
            print("Creando nueva base de datos...")
            db.create_all()
            
            try:
                admin = Usuario.query.filter_by(username="admin").first()
                user = Usuario.query.filter_by(username="user").first()
                
                if not admin:
                    admin = Usuario(username="admin", password="adminpass")
                    db.session.add(admin)
                    print("Usuario admin creado")
                
                if not user:
                    user = Usuario(username="user", password="userpass")
                    db.session.add(user)
                    print("Usuario user creado")
                
                db.session.commit()

                proyectos_default = [
                    {
                        'titulo': "Práctica 1: Texas Hold'em",
                        'autor': 'Koral Tubía y Sonia Aoi García',
                        'fecha': '2022-06-12',
                        'descripcion': "En la Práctica 1 se desarrolló un juego de Texas Hold'em, una variante popular del póker. El juego permite a los jugadores recibir dos cartas ocultas y combinar estas con cinco cartas comunitarias para formar la mejor mano posible. Se implementaron las reglas básicas del juego, incluyendo las rondas de apuestas y la evaluación de manos, para crear una experiencia interactiva.",
                        'imagen_url': 'https://as2.ftcdn.net/v2/jpg/00/17/91/51/1000_F_17915136_uGjZaU5JlpAmsGhAYGg67EmRWZTR5OWp.jpg',
                        'usuario_id': admin.id
                    },
                    {
                        'titulo': 'Práctica 2: El juego de la vida',
                        'autor': 'Koral Tubia y Sonia Aoi Garcia',
                        'fecha': '2023-02-01',
                        'descripcion': 'En la Práctica 2 se implementó el Juego de la Vida, un autómata celular diseñado por John Horton Conway en 1970. Este juego se desarrolla en una cuadrícula donde cada celda representa una célula que evoluciona según reglas específicas. En cada turno, el estado del mundo se determina por el estado inicial de las células, las reglas de evolución y el número de turnos transcurridos.',
                        'imagen_url': 'https://media.licdn.com/dms/image/v2/D5612AQHkZL5tMuHhfA/article-cover_image-shrink_600_2000/article-cover_image-shrink_600_2000/0/1683392101730?e=2147483647&v=beta&t=TYHnslquYAwSyc84EHQB9wCX7dPRzb1qUk5slf1RDX0 ',
                        'usuario_id': admin.id
                    },
                    {
                        'titulo': 'Práctica 3: Programación lógica',
                        'autor': 'Koral Tubía y Sonia Aoi García',
                        'fecha': ' 2023-02-05',
                        'descripcion': 'En la Práctica 3 de Programación Lógica, se desarrollaron reglas en Prolog para representar y consultar conexiones entre provincias a través de carreteras. Se realizaron trazas de consultas, se modificaron reglas para permitir conexiones bidireccionales y se implementaron funciones recursivas para evitar ciclos en la búsqueda de rutas. También se desarrollaron reglas para calcular distancias entre provincias y se demostraron ejemplos de su funcionamiento.',
                        'imagen_url': 'https://ih1.redbubble.net/image.4668425849.4989/ur,pin_large_front,square,600x600.jpg',
                        'usuario_id': admin.id
                    }
                ]

                if not Proyecto.query.first():
                    for proyecto_data in proyectos_default:
                        proyecto = Proyecto(**proyecto_data)
                        db.session.add(proyecto)
                    
                    db.session.commit()
                    print("Proyectos por defecto creados")
                
                print("Base de datos inicializada correctamente")
                
            except Exception as e:
                db.session.rollback()
                print(f"Error durante la inicialización: {str(e)}")
    else:
        print(f"Base de datos {DB_NAME} ya existe")


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    user = Usuario.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=1))
        return jsonify(access_token=token), 200
    return jsonify({"msg": "Credenciales incorrectas"}), 401


@app.route('/api/proyectos', methods=['POST'])
@jwt_required()
def agregar_proyecto():
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        print(f"Datos recibidos: {data}")  
        print(f"Usuario ID: {current_user_id}") 
        
        nuevo_proyecto = Proyecto(
            titulo=data['titulo'],
            autor=data['autor'],
            fecha=data['fecha'],
            descripcion=data['descripcion'],
            imagen_url=data.get('imagen_url'),
            usuario_id=current_user_id
        )
        
        db.session.add(nuevo_proyecto)
        db.session.commit()
        

        return jsonify({
            "msg": "Proyecto añadido exitosamente",
            "proyecto": {
                "id": nuevo_proyecto.id,
                "titulo": nuevo_proyecto.titulo,
                "autor": nuevo_proyecto.autor,
                "fecha": nuevo_proyecto.fecha,
                "descripcion": nuevo_proyecto.descripcion,
                "imagen_url": nuevo_proyecto.imagen_url
            }
        }), 201
    except Exception as e:
        print(f"Error al agregar proyecto: {str(e)}")
        db.session.rollback()
        return jsonify({"msg": f"Error al agregar proyecto: {str(e)}"}), 400


@app.route('/api/proyectos', methods=['GET'])
def obtener_proyectos():  
    proyectos = Proyecto.query.all()  
    proyectos_data = [{
        "id": p.id,
        "titulo": p.titulo,
        "autor": p.autor,
        "fecha": p.fecha,
        "descripcion": p.descripcion,
        "imagen_url": p.imagen_url
    } for p in proyectos]
    return jsonify(proyectos_data), 200

@app.route('/api/proyectos/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_proyecto(id):
    current_user_id = get_jwt_identity()
    proyecto = Proyecto.query.get(id)
    
    if proyecto and proyecto.usuario_id == current_user_id:
        db.session.delete(proyecto)
        db.session.commit()
        return jsonify({"msg": "Proyecto eliminado"}), 200
    return jsonify({"msg": "Proyecto no encontrado o no autorizado"}), 404


@app.route('/api/proyectos/<int:id>', methods=['PUT'])
@jwt_required()
def editar_proyecto(id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    

    proyecto = Proyecto.query.get(id)
    if not proyecto or proyecto.usuario_id != current_user_id:
        return jsonify({"msg": "Proyecto no encontrado o no autorizado"}), 404


    proyecto.titulo = data.get('titulo', proyecto.titulo)
    proyecto.autor = data.get('autor', proyecto.autor)
    proyecto.fecha = data.get('fecha', proyecto.fecha)
    proyecto.descripcion = data.get('descripcion', proyecto.descripcion)
    proyecto.imagen_url = data.get('imagen_url', proyecto.imagen_url)

    try:
        db.session.commit()
        return jsonify({"msg": "Proyecto actualizado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error al actualizar proyecto: {str(e)}"}), 400


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

