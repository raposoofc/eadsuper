# src/model/user.py

class User:  # É a classe que representa um usuário.
    """
    Classe para representar a entidade Usuário no sistema.
    """
    def __init__(self, nome, cpf, telefone, email, nomeUsuario, senha, role='user'): # __init__ é o construtor da classe.
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email
        self.nomeUsuario = nomeUsuario
        self.senha = senha  # É automaticamente alterada para um hash da senha
        self.role = role    # Função que tem um valor padrão de'user' sempre que não for especificado um tipo diferente.

    def to_dict(self): # Ele converte o objeto User em um dicionário.
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