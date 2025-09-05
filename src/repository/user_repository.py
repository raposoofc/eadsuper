# src/repository/user_repository.py

import json
import os

# Caminho do arquivo de banco de dados JSON
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'data.json') # Define o caminho para o arquivo de dados.

def load_data(): # Carrega os dados do arquivo JSON.
    """Carrega os dados do arquivo JSON."""
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou for inválido, retorna uma estrutura vazia
        return {"users": []} # Retorna uma estrutura vazia se o arquivo não existir ou for inválido. Evita erros.

def save_data(data): # Salva os dados no arquivo JSON.
    """Salva os dados no arquivo JSON."""
    with open(DB_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def get_all_users(): # Retorna a lista completa de usuários.
    """Retorna a lista completa de usuários."""
    data = load_data()
    return data["users"]

def add_user(new_user): # Adiciona um novo usuário ao banco de dados.
    """Adiciona um novo usuário ao banco de dados."""
    data = load_data()
    data['users'].append(new_user)
    save_data(data)

def get_user_by_email_or_username(identifier): # Busca um usuário por e-mail ou nome de usuário.
    """Busca um usuário por e-mail ou nome de usuário."""
    data = load_data()
    for user in data["users"]:
        if user["email"] == identifier or user["nomeUsuario"] == identifier:
            return user
    return None

def delete_user_by_email(email): # Exclui um usuário pelo e-mail. Ele retorna True se encontrou e removeu o usuário e False caso contrário.
    """Exclui um usuário pelo e-mail e retorna True se a exclusão foi bem-sucedida."""
    data = load_data()
    initial_count = len(data["users"])
    data["users"] = [user for user in data["users"] if user["email"] != email]
    
    if len(data["users"]) < initial_count:
        save_data(data)
        return True
    return False