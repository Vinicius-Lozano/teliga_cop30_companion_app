# Te Liga! API

Bem-vindo ao projeto "Te Liga!". O app visa construir uma melhor experiência para turistas e interessados durante o evento da COP30, servindo como um companion com várias funções e interações com a cidade, o evento e a cultura local.
Através de sistemas integrados como uma lista estilo Pokédex com peculiaridades da região (animais, plantas e pautas da COP30)

## Tecnologias Utilizadas

- **Python 3.10+**
- **Django 5.2+**
- **Django REST Framework**: Para a construção da API REST.
- **Simple JWT**: Para autenticação baseada em JSON Web Tokens.
- **drf-spectacular**: Para geração automática da documentação OpenAPI (Swagger UI).
- **django-cors-headers**: Para gerenciar o Cross-Origin Resource Sharing (CORS).
- **SQLite**: Banco de dados padrão para desenvolvimento.

---

## Guia de Instalação e Setup

Siga este passo a passo para configurar e rodar o ambiente de desenvolvimento localmente.

### Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados na sua máquina:
- [Git](https://git-scm.com/)
- [Python 3.10 ou superior](https://www.python.org/downloads/)

### 1. Clonar o Repositório

Abra seu terminal, navegue até o diretório onde deseja salvar o projeto e clone o repositório.

```bash
git clone <URL_DO_SEU_REPOSITORIO_GIT>
cd projeto_te_liga
```

### 2. Criar e Ativar o Ambiente Virtual (`venv`)

É uma prática essencial isolar as dependências do projeto.

```bash
# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente (Windows - PowerShell/CMD)
.\venv\Scripts\activate

# Ative o ambiente (Linux/macOS)
# source venv/bin/activate
```

Seu prompt do terminal deve agora mostrar `(venv)` no início.

### 3. Instalar as Dependências

Com o ambiente ativado, instale todos os pacotes necessários que estão listados no arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```
### 5. Aplicar as Migrações do Banco de Dados

Este comando cria as tabelas no banco de dados (por padrão, o arquivo `db.sqlite3`).

```bash
python manage.py migrate
```

### 6. Criar um Superusuário

Crie um usuário administrador para acessar o painel de admin do Django. Siga as instruções no terminal.

```bash
python manage.py createsuperuser
```

### 7. Rodar o Servidor de Desenvolvimento

Tudo pronto! Inicie o servidor.

```bash
python manage.py runserver
```

## Acessando a Aplicação

- **API e Documentação (Swagger UI)**: Abra seu navegador e acesse http://127.0.0.1:8000/
- **Painel de Admin**: Acesse http://127.0.0.1:8000/admin/ e faça login com as credenciais do superusuário que você criou.
