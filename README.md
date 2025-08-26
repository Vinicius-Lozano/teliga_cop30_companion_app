# Projeto Te Liga! 🌎

Bem-vindo ao repositório oficial do projeto "Te Liga!", uma aplicação full-stack com backend em Django e frontend em Quasar/Vue.

Este guia foi feito para ajudar qualquer pessoa a configurar e rodar o projeto em sua máquina local.

## 📋 Pré-requisitos

Antes de começar, garanta que você tenha os seguintes programas instalados em seu computador:

*   [Git](https://git-scm.com/downloads)
*   [Python](https://www.python.org/downloads/) (versão 3.10 ou superior)
*   [Node.js](https://nodejs.org/en/) (versão 18 ou superior, que inclui o `npm`)

## 🚀 Instalação e Configuração

Siga estes passos para ter o projeto rodando. Todos os comandos devem ser executados no seu terminal (como PowerShell, CMD ou Git Bash).

### 1. Clone o Repositório

Primeiro, crie uma cópia do projeto na sua máquina:

```bash
git clone https://github.com/Vinicius-Lozano/projeto_te_liga.git
cd projeto_te_liga
```

### 2. Instale Todas as Dependências

Nós criamos um script que instala tudo o que você precisa (tanto para o backend quanto para o frontend) com um único comando. Ele também irá configurar o ambiente virtual do Python (`venv`).

```bash
npm install
```
Este comando pode demorar um pouco na primeira vez, pois está baixando todas as bibliotecas necessárias.

## ▶️ Executando o Projeto

Para iniciar os servidores de desenvolvimento do backend e do frontend ao mesmo tempo, use o seguinte comando:

```bash
npm run dev
```

Seu terminal mostrará os logs de ambos os servidores. Agora, você pode acessar as diferentes partes da aplicação no seu navegador:

*   **Frontend (Sua Aplicação Quasar/Vue):**
    *   `http://localhost:9000` (ou a porta indicada no terminal)

*   **Backend (Ferramentas do Django):**
    *   **Painel de Admin:** `http://localhost:8000/admin`
    *   **Documentação da API (Swagger):** `http://localhost:8000/api/swagger/`

Para parar os servidores, pressione `Ctrl + C` no terminal.

## 🌳 Git Workflow: Como Contribuir Corretamente

Para manter nosso projeto organizado e evitar problemas, **NUNCA envie alterações diretamente para a branch `main`**. Siga este fluxo de trabalho:

### 1. Crie sua Própria Branch

Antes de começar a codificar, crie uma nova branch a partir da `main`. Use um nome descritivo, como seu nome e o que você vai fazer.

```bash
# Garanta que você está na branch main e com a versão mais recente
git checkout main
git pull origin main

# Crie sua nova branch
git checkout -b seu-nome/descricao-da-tarefa
```
**Exemplo:** `git checkout -b vinicius/tela-de-login`

### 2. Faça suas Alterações e Commits

Agora você está na sua branch! Pode codificar à vontade. Quando terminar uma parte do trabalho, salve suas alterações no Git.

```bash
# Adiciona todos os arquivos modificados para serem salvos
git add .

# Cria um "ponto de salvamento" com uma mensagem clara
git commit -m "feat: Adiciona o formulário de login na tela inicial"
```

### 3. Envie sua Branch para o GitHub

Para que outras pessoas possam ver seu trabalho (e para você criar um Pull Request), envie sua branch para o repositório remoto.

```bash
git push -u origin seu-nome/descricao-da-tarefa
```
**Exemplo:** `git push -u origin vinicius/tela-de-login`

### 4. Abra um Pull Request (PR)

Depois de enviar sua branch, vá até a página do projeto no GitHub. Você verá um aviso para criar um **Pull Request**. Clique nele, adicione uma descrição do que você fez e peça para um colega revisar seu código.