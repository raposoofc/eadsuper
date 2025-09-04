# app.py
import os
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from functools import wraps

# Importa o Blueprint do seu controlador
from src.controller.user_controller import user_blueprint

# Define o caminho base do projeto para que o Flask encontre os arquivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cria a instância da aplicação Flask com a nova configuração de caminhos
app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'src', 'static'),
            template_folder=os.path.join(BASE_DIR, 'src', 'templates'))

# Configura uma chave secreta para a sessão
app.secret_key = 'sua_chave_secreta_aqui' # Substitua isso por uma chave segura

# =================================================================
#  Função Decoradora para Proteção de Rotas
# =================================================================

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verifica se o usuário está na sessão
            if 'user' not in session:
                return redirect(url_for('entrar'))

            # Se o login for bem-sucedido, mas o role for restrito
            user = session.get('user')
            if role and user['role'] != role:
                return redirect(url_for('painel_aluno'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator

# =ata============================================================
#  Rotas da Aplicação (Frontend)
# =================================================================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/entrar")
def entrar():
    return render_template("login_cadastro.html")

@app.route("/painel_aluno")
@login_required() # Protege a rota, exigindo que o usuário esteja logado
def painel_aluno():
    return render_template("painel_aluno.html")

@app.route("/painel_admin")
@login_required(role='admin') # Protege a rota, exigindo que o usuário seja 'admin'
def painel_admin():
    return render_template("painel_admin.html")

# =================================================================
#  Rotas de Logout
# =================================================================
@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# =================================================================
#  Registra os Blueprints da API (Backend)
# =================================================================

app.register_blueprint(user_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)