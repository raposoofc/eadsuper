# src/controller/user_controller.py

from flask import request, jsonify, Blueprint, session, redirect, url_for
from ..service.user_service import UserService

user_blueprint = Blueprint('user_controller', __name__, url_prefix='/api')
user_service = UserService()

@user_blueprint.route("/cadastro", methods=["POST"])
def cadastro():
    user_data = request.get_json()
    response = user_service.register_user(user_data)
    
    if response["success"]:
        return jsonify({"message": response["message"]}), 201
    else:
        return jsonify({"message": response["message"]}), 409

@user_blueprint.route("/login", methods=["POST"]) # rota de login
def login():
    credentials = request.get_json()
    response = user_service.authenticate_user(
        credentials['email_or_user'],
        credentials['senha']
    )
    
    if response["success"]:
        user = response["user"]
        session['user'] = user
        session['user'].pop('senha', None)
        
        if user['role'] == 'admin':
            return jsonify({"message": "Login realizado com sucesso!", "redirect": url_for('painel_admin')}), 200
        else:
            return jsonify({"message": "Login realizado com sucesso!", "redirect": url_for('painel_aluno')}), 200
    else:
        return jsonify({"message": response["message"]}), 401

@user_blueprint.route("/users", methods=["GET"])
def get_users():
    users = user_service.get_all_users()
    return jsonify(users), 200

@user_blueprint.route("/users/<string:email>", methods=["DELETE"])
def delete_user(email):
    response = user_service.delete_user(email)
    
    if response["success"]:
        return jsonify({"message": response["message"]}), 200
    else:
        return jsonify({"message": response["message"]}), 404

# --- NOVA ROTA DE ATUALIZAÇÃO ---
@user_blueprint.route("/users/<string:email>", methods=["PUT"])
def update_user(email):
    user_data = request.get_json()
    response = user_service.update_user(email, user_data)
    if response["success"]:
        return jsonify({"message": response["message"]}), 200
    else:
        return jsonify({"message": response["message"]}), 404

@user_blueprint.route("/current_user", methods=["GET"])
def current_user():
    if 'user' in session:
        return jsonify(session['user']), 200
    return jsonify({"message": "Nenhum usuário logado."}), 404

# --- ROTAS DE EXPORTAÇÃO ---
@user_blueprint.route("/export/xlsx", methods=["GET"])
def export_xlsx():
    response = user_service.export_users_to_xlsx()
    if response["success"]:
        return response["file"], 200, {
            'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'Content-Disposition': 'attachment; filename=usuarios.xlsx'
        }
    else:
        return jsonify({"message": response["message"]}), 500

@user_blueprint.route("/export/pdf", methods=["GET"])
def export_pdf():
    response = user_service.export_users_to_pdf()
    if response["success"]:
        return response["file"], 200, {
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'attachment; filename=usuarios.pdf'
        }
    else:
        return jsonify({"message": response["message"]}), 500