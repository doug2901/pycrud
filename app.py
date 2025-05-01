from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from os import environ
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# VARIAVEIS DE AMBIENTE
#OBRIGATÓRIAS:
# DB_URL: URL do banco de dados (ex: postgresql://USER:PASSWORD@HOST:PORT/DB_NAME)  

#OPTCIONAIS:
# APP_PORT: Porta que o app irá rodar (default: 5000)
# SWAGGER_TITLE: Título da documentação Swagger (default: User Management API)
# SWAGGER_DESCRIPTION: Descrição da documentação Swagger (default: API para gerenciamento de usuários - projeto de estudos CKAD)
# SWAGGER_VERSION: Versão da documentação Swagger (default: 1.0.0)
# SWAGGER_ORG: Organização responsável pela documentação Swagger (default: Seu Nome ou Empresa)
# SWAGGER_DEV: Desenvolvedor responsável pela documentação Swagger (default: Seu Nome)
# SWAGGER_EMAIL: Email do desenvolvedor responsável pela documentação Swagger (default: seuemail@example.com)
#SWAGGER_SCHEME: Esquema da documentação Swagger (default: http, https)

# Logging
logging.basicConfig(level=logging.INFO)

# Swagger configuration
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": environ.get('SWAGGER_TITLE', 'User Management API'),
        "description": environ.get('SWAGGER_DESCRIPTION', 'API para gerenciamento de usuários - projeto de estudos CKAD'),
        "version": environ.get('SWAGGER_VERSION', '1.0.0'),
        "contact": {
            "responsibleOrganization": environ.get('SWAGGER_ORG', 'Seu Nome ou Empresa'),
            "responsibleDeveloper": environ.get('SWAGGER_DEV', 'Seu Nome'),
            "email": environ.get('SWAGGER_EMAIL', 'seuemail@example.com'),
            "url": environ.get('SWAGGER_URL', 'https://seusite.com'),
        },
    },
    "basePath": "/",
    "schemes": [
        environ.get('SWAGGER_SCHEME', 'http'),
        environ.get('SWAGGER_SCHEME', 'https')
    ],
}

#swagger = Swagger(app, template=swagger_template)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # incluir todas rotas
            "model_filter": lambda tag: True,  # incluir todos models
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)
##########

db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}

with app.app_context():
    db.create_all()

# Healthcheck route
@app.route('/health', methods=['GET'])
def health():
    """
    Health Check
    ---
    tags:
      - Health
    responses:
      200:
        description: App is healthy
    """
    return make_response(jsonify({'status': 'ok'}), 200)

# Create a user
@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - email
            properties:
              username:
                type: string
              email:
                type: string
    responses:
      201:
        description: User created
      500:
        description: Error creating user
    """
    try:
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'user created'}), 201)
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        return make_response(jsonify({'message': 'error creating user'}), 500)

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    """
    Get all users
    ---
    tags:
      - Users
    responses:
      200:
        description: A list of users
    """
    try:
        users = User.query.all()
        return make_response(jsonify([user.json() for user in users]), 200)
    except Exception as e:
        logging.error(f"Error getting users: {e}")
        return make_response(jsonify({'message': 'error getting users'}), 500)

# Get a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """
    Get a user by ID
    ---
    tags:
      - Users
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the user
    responses:
      200:
        description: User found
      404:
        description: User not found
      500:
        description: Error getting user
    """
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'user': user.json()}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        logging.error(f"Error getting user: {e}")
        return make_response(jsonify({'message': 'error getting user'}), 500)

# Update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    """
    Update a user by ID
    ---
    tags:
      - Users
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the user
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - email
            properties:
              username:
                type: string
              email:
                type: string
    responses:
      200:
        description: User updated
      404:
        description: User not found
      500:
        description: Error updating user
    """
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message': 'user updated'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        logging.error(f"Error updating user: {e}")
        return make_response(jsonify({'message': 'error updating user'}), 500)

# Delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """
    Delete a user by ID
    ---
    tags:
      - Users
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the user
    responses:
      200:
        description: User deleted
      404:
        description: User not found
      500:
        description: Error deleting user
    """
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'user deleted'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        logging.error(f"Error deleting user: {e}")
        return make_response(jsonify({'message': 'error deleting user'}), 500)

if __name__ == "__main__":
    port = int(environ.get('APP_PORT', 5000))
    app.run(host='0.0.0.0', port=port)