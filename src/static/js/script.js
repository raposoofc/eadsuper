// script.js

document.addEventListener('DOMContentLoaded', () => {

    // Lógica de Alternância das Telas de Login/Cadastro
    const container = document.getElementById('container');
    const registerBtn = document.getElementById('register');
    const loginBtn = document.getElementById('login');

    if (container && registerBtn && loginBtn) {
        registerBtn.addEventListener('click', () => {
            container.classList.add("active");
        });

        loginBtn.addEventListener('click', () => {
            container.classList.remove("active");
        });
    }

    // Lógica para Autenticação e CRUD (Comunicação com o Flask)
    function setupAuthForms() {
        const cadastroForm = document.getElementById('cadastroForm');
        if (cadastroForm) {
            cadastroForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const data = {
                    nome: document.getElementById('nomeCompleto').value,
                    cpf: document.getElementById('cpf').value,
                    telefone: document.getElementById('telefone').value,
                    email: document.getElementById('email').value,
                    nomeUsuario: document.getElementById('nomeUsuario').value,
                    senha: document.getElementById('senhaCadastro').value
                };

                const response = await fetch('/api/cadastro', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                alert(result.message);
                if (response.ok) {
                    container.classList.remove("active");
                }
            });
        }

        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const credentials = {
                    email_or_user: document.getElementById('loginUsuario').value,
                    senha: document.getElementById('loginSenha').value
                };

                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(credentials)
                });

                const result = await response.json();
                alert(result.message);

                if (response.ok) {
                    if (result.redirect) {
                        window.location.href = result.redirect;
                    }
                }
            });
        }
    }

    // Lógica para os Painéis
    function setupPanelLogic() {
        const path = window.location.pathname;
        
        if (path === '/painel_aluno') {
            const userNameElement = document.getElementById('userName');
            const userNomeElement = document.getElementById('userNome');
            const userEmailElement = document.getElementById('userEmail');
            const userNomeUsuarioElement = document.getElementById('userNomeUsuario');
            const userCpfElement = document.getElementById('userCpf');
            const userTelefoneElement = document.getElementById('userTelefone');

            fetch('/api/current_user')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Usuário não autenticado.');
                    }
                    return response.json();
                })
                .then(user => {
                    if (userNameElement) userNameElement.textContent = user.nome;
                    if (userNomeElement) userNomeElement.textContent = user.nome;
                    if (userEmailElement) userEmailElement.textContent = user.email;
                    if (userNomeUsuarioElement) userNomeUsuarioElement.textContent = user.nomeUsuario;
                    if (userCpfElement) userCpfElement.textContent = user.cpf;
                    if (userTelefoneElement) userTelefoneElement.textContent = user.telefone;
                })
                .catch(error => {
                    console.error("Erro ao obter dados do usuário logado:", error);
                });
        }

        if (path === '/painel_admin') {
            const adminFormContainer = document.getElementById('adminFormContainer');
            const adminForm = document.getElementById('adminForm');
            const addAdminBtn = document.getElementById('addAdminBtn');
            const cancelAdminBtn = document.getElementById('cancelAdminBtn');
            const adminTableBody = document.querySelector('#adminTable tbody');
            const formTitle = document.getElementById('formTitle');
            const adminSenhaGroup = document.getElementById('adminSenhaGroup');
            const sidebarToggleBtn = document.getElementById('sidebarToggle');
            const sidebar = document.querySelector('.sidebar');
            const exportBtn = document.querySelector('.btn-export');

            let currentAdminEmail = null;

            sidebarToggleBtn.addEventListener('click', () => {
                sidebar.classList.toggle('collapsed');
            });

            addAdminBtn.addEventListener('click', () => {
                adminFormContainer.classList.remove('hidden');
                adminForm.reset();
                formTitle.textContent = 'Adicionar Novo Administrador';
                adminSenhaGroup.style.display = 'block';
                currentAdminEmail = null;
            });

            cancelAdminBtn.addEventListener('click', () => {
                adminFormContainer.classList.add('hidden');
            });

            adminForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const adminData = {
                    nome: document.getElementById('adminNomeCompleto').value,
                    email: document.getElementById('adminEmail').value,
                    nomeUsuario: document.getElementById('adminNomeUsuario').value,
                    cpf: document.getElementById('adminCpf').value,
                    telefone: document.getElementById('adminTelefone').value,
                    role: document.getElementById('adminRole').value,
                };

                const url = currentAdminEmail ? `/api/users/${currentAdminEmail}` : '/api/cadastro';
                const method = currentAdminEmail ? 'PUT' : 'POST';
                
                if (!currentAdminEmail) {
                    adminData.senha = document.getElementById('adminSenha').value;
                }

                const response = await fetch(url, {
                    method: method,
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(adminData)
                });

                const result = await response.json();
                alert(result.message);

                if (response.ok) {
                    adminFormContainer.classList.add('hidden');
                    fetchAdmins();
                }
            });

            async function fetchAdmins() {
                const response = await fetch('/api/users');
                if (response.ok) {
                    const users = await response.json();
                    renderAdminTable(users);
                } else {
                    alert('Erro ao carregar a lista de usuários.');
                }
            }

            function renderAdminTable(users) {
                adminTableBody.innerHTML = '';
                users.forEach(user => {
                    const row = adminTableBody.insertRow();
                    row.innerHTML = `
                        <td>${user.nome}</td>
                        <td>${user.email}</td>
                        <td>${user.nomeUsuario}</td>
                        <td>${user.role}</td>
                        <td>
                            <button class="edit-btn btn secondary" data-email="${user.email}"><i class="fas fa-edit"></i> Editar</button>
                            <button class="delete-btn btn danger" data-email="${user.email}"><i class="fas fa-trash-alt"></i> Excluir</button>
                        </td>
                    `;
                });

                document.querySelectorAll('.delete-btn').forEach(button => {
                    button.addEventListener('click', async (e) => {
                        const emailToDelete = e.target.dataset.email;
                        if (confirm(`Tem certeza que deseja excluir o usuário com e-mail ${emailToDelete}?`)) {
                            const response = await fetch(`/api/users/${emailToDelete}`, {
                                method: 'DELETE'
                            });
                            const result = await response.json();
                            alert(result.message);
                            if (response.ok) {
                                fetchAdmins();
                            }
                        }
                    });
                });

                document.querySelectorAll('.edit-btn').forEach(button => {
                    button.addEventListener('click', async (e) => {
                        const emailToEdit = e.target.dataset.email;
                        const userToEdit = users.find(u => u.email === emailToEdit);
                        
                        if (userToEdit) {
                            document.getElementById('adminNomeCompleto').value = userToEdit.nome;
                            document.getElementById('adminEmail').value = userToEdit.email;
                            document.getElementById('adminNomeUsuario').value = userToEdit.nomeUsuario;
                            document.getElementById('adminCpf').value = userToEdit.cpf;
                            document.getElementById('adminTelefone').value = userToEdit.telefone;
                            document.getElementById('adminRole').value = userToEdit.role;
                            
                            adminSenhaGroup.style.display = 'none';

                            formTitle.textContent = 'Editar Administrador';
                            currentAdminEmail = userToEdit.email;
                            adminFormContainer.classList.remove('hidden');
                        }
                    });
                });
            }

            if (exportBtn) {
                exportBtn.addEventListener('click', () => {
                    const format = prompt("Deseja exportar para PDF ou XLSX? Digite 'pdf' ou 'xlsx'.");
                    if (format && (format.toLowerCase() === 'pdf' || format.toLowerCase() === 'xlsx')) {
                        window.location.href = `/api/export/${format.toLowerCase()}`;
                    } else {
                        alert("Formato inválido. Por favor, digite 'pdf' ou 'xlsx'.");
                    }
                });
            }
            
            fetchAdmins();
        }
    }

    // Inicializa todas as lógicas
    setupAuthForms();
    setupPanelLogic();
});