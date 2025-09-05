# EAD Super

Este é um projeto de um sistema de Ensino a Distância (EAD) simples, desenvolvido em Python com o framework Flask.

## Funcionalidades Implementadas
- **Página Inicial (Landing Page):** Uma apresentação visual dos cursos com cards estáticos e um layout otimizado.
- **Autenticação de Usuários:** Funcionalidades de login e cadastro.
- **Painel do Aluno:** Uma área restrita onde o aluno pode visualizar seus dados cadastrais em um formato de ficha.
- **Painel do Administrador:** Uma área restrita para o administrador, com um layout de cards similar ao do aluno.
- **Responsividade:** O layout de todas as páginas se adapta a diferentes tamanhos de tela (desktop, tablet e smartphone).

## Estrutura do Projeto
O projeto foi organizado em um modelo de arquitetura por camadas para garantir a separação de responsabilidades e a manutenibilidade do código. Os dados são persistidos em arquivos JSON.

---

## Como Rodar o Projeto

Siga os passos abaixo para executar o projeto em seu ambiente local.

### Pré-requisitos
- Python 3.x
- Git (opcional, para clonar o repositório)

### Passos

1. **Clone o repositório:**
   ```bash
  git clone [https://github.com/raposoofc/eadsuper](https://github.com/raposoofc/eadsuper)
  cd eadsuper
  
2. Crie e ative o ambiente virtual:

python -m venv venv
# No Windows
.\venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate
Instale as dependências:

3. Instale as dependências:

pip install -r requirements.txt
Execute a aplicação:

4. Execute a aplicação:

python app.py

---

A aplicação estará disponível em http://127.0.0.1:5000.
