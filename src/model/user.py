# src/model/user.py

class User:
    """
    Classe para representar a entidade Usuário no sistema.
    """
    def __init__(self, nome, cpf, telefone, email, nomeUsuario, senha, role='user'):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.nomeUsuario = nomeUsuario
        self.senha = senha  # Futuramente, será um hash da senha
        self.role = role    # 'user' ou 'admin'

    def to_dict(self):
        """Converte o objeto User para um dicionário para serialização em JSON."""
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "telefone": self.telefone,
            "email": self.email,
            "nomeUsuario": self.nomeUsuario,
            "senha": self.senha,
            "role": self.role
        }