# src/service/user_service.py

import re
import io
from flask_bcrypt import Bcrypt 
from ..repository import user_repository
from ..model.user import User

from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER


bcrypt = Bcrypt() # bcrypt: Objeto para lidar com a criptografia de senhas. A criptografia é usada para que a senha real do usuário nunca seja armazenada em texto puro, aumentando a segurança.

# Registra uma fonte que suporta caracteres acentuados
try:
    registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
except:
    pass # A fonte pode não estar disponível no ambiente, mas o código continua.

class UserService:
    def __init__(self):
        self.repository = user_repository

    def validate_password(self, senha): # Valida se a senha atende aos critérios de segurança
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+=\-{}[\]|\\:;\"'<,>.?/])(.{6,12})$"
        return re.match(regex, senha)

    def register_user(self, user_data): # Registra um novo usuário.
        if self.repository.get_user_by_email_or_username(user_data.get('email')) or \
           self.repository.get_user_by_email_or_username(user_data.get('nomeUsuario')):
            return {"success": False, "message": "Nome de usuário ou e-mail já cadastrados."}
        
        senha_hash = bcrypt.generate_password_hash(user_data['senha']).decode('utf-8') # Gera o hash da senha para armazenamento seguro.
        
        new_user = User( # Cria uma nova instância do usuário com os dados fornecidos.
            nome=user_data.get('nome'),
            cpf=user_data.get('cpf'),
            telefone=user_data.get('telefone'),
            email=user_data.get('email'),
            nomeUsuario=user_data.get('nomeUsuario'),
            senha=senha_hash,
            role=user_data.get('role', 'user')
        )
        
        self.repository.add_user(new_user.to_dict())
        return {"success": True, "message": "Cadastro realizado com sucesso!"}

    def authenticate_user(self, identifier, senha): # Autentica um usuário com base no e-mail ou nome de usuário e senha.
        user = self.repository.get_user_by_email_or_username(identifier)
        if user and bcrypt.check_password_hash(user['senha'], senha): # Verifica se a senha fornecida corresponde ao hash armazenado.
            return {"success": True, "user": user}
        return {"success": False, "message": "Credenciais inválidas."}

    def update_user(self, email, updated_data): # Atualiza os dados do usuário, exceto a senha.
        data = self.repository.load_data()
        found_user = next((u for u in data['users'] if u['email'] == email), None)
        
        if not found_user:
            return {"success": False, "message": "Usuário não encontrado."}
        
        for key, value in updated_data.items():
            if key != 'senha':
                found_user[key] = value
        
        self.repository.save_data(data)
        return {"success": True, "message": "Dados do usuário atualizados com sucesso."}

    def get_all_users(self):
        return self.repository.get_all_users()
        
    def delete_user(self, email):
        if self.repository.delete_user_by_email(email):
            return {"success": True, "message": "Usuário excluído com sucesso."}
        return {"success": False, "message": "Usuário não encontrado."}

    def export_users_to_xlsx(self): # Exporta os dados dos usuários para um arquivo XLSX.
        try:
            users_data = self.repository.get_all_users()
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Usuários"
            
            headers = ["Nome Completo", "E-mail", "Nome de Usuário", "CPF", "Telefone", "Função"]
            sheet.append(headers)

            for user in users_data:
                sheet.append([
                    user.get("nome", ""),
                    user.get("email", ""),
                    user.get("nomeUsuario", ""),
                    user.get("cpf", ""),
                    user.get("telefone", ""),
                    user.get("role", "")
                ])

            file_stream = io.BytesIO()
            workbook.save(file_stream)
            file_stream.seek(0)
            
            return {"success": True, "file": file_stream}
        except Exception as e:
            return {"success": False, "message": f"Erro ao exportar para XLSX: {e}"}

    def export_users_to_pdf(self): # Exporta os dados dos usuários para um arquivo PDF.
        try:
            users_data = self.repository.get_all_users()
            file_stream = io.BytesIO()
            doc = SimpleDocTemplate(file_stream, pagesize=A4)
            styles = getSampleStyleSheet()

            # Estilo personalizado para o título com fonte que suporta acentuação
            styles.add(ParagraphStyle(name='CustomTitle', fontSize=18, leading=22, alignment=TA_CENTER, fontName='DejaVuSans', spaceAfter=12))

            elements = []
            title = Paragraph("Relatório de Usuários Cadastrados", styles['CustomTitle'])
            elements.append(title)
            
            table_data = [["Nome Completo", "E-mail", "Usuário", "Função"]]
            for user in users_data:
                table_data.append([
                    user.get("nome", ""),
                    user.get("email", ""),
                    user.get("nomeUsuario", ""),
                    user.get("role", "")
                ])
                
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold')
            ])
            
            pdf_table = Table(table_data)
            pdf_table.setStyle(table_style)
            elements.append(pdf_table)
            
            doc.build(elements)
            file_stream.seek(0)
            
            return {"success": True, "file": file_stream}
        except Exception as e:
            return {"success": False, "message": f"Erro ao exportar para PDF: {e}"}