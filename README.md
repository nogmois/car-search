# Car Search

Projeto de busca de carros via protocolo MCP.

## Setup

1. Crie e ative o venv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .\.venv\Scripts\activate    # Windows
   ```

# Car Search

Projeto de busca de carros via protocolo TCP (MCP) com CLI interativa e Docker.

## 🔗 Clonar o repositório

```bash
git clone <URL_DO_REPO> car_search
cd car_search
```

## ⚙️ Configuração via terminal (sem Docker)

1. Crie e ative o ambiente virtual:

   - **Linux/macOS**:

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

   - **Windows (PowerShell)**:

     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

   - **Windows (CMD)**:

     ```cmd
     python -m venv .venv
     .\.venv\Scripts\activate
     ```

2. Instale as dependências:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Copie e edite o arquivo de variáveis de ambiente:

   ```bash
   cp .env.example .env     # Linux/macOS
   copy .env.example .env   # Windows
   ```

   Edite `.env` com sua URL do Postgres.

4. Crie o banco no PostgreSQL (via psql, PgAdmin ou DBeaver):

   ```sql
   CREATE DATABASE car_search_db;
   ```

5. Rode as migrações:

   ```bash
   alembic upgrade head
   ```

6. Popule dados de exemplo:

   ```bash
   python -m app.scripts.populate_db --number 100
   ```

7. Inicie o servidor MCP:

   ```bash
   python -m app.mcp.server --host 127.0.0.1 --port 5000
   ```

8. Em outro terminal, rode a CLI:

   ```bash
   python -m app.cli.main
   ```

9. Executar testes:

   ```bash
   pytest
   ```

## 🐳 Configuração via Docker

1. Instale Docker e Docker Compose.

2. No diretório do projeto, rode:

   ```bash
   docker-compose down -v      # remove containers, redes e volumes
   docker-compose up --build
   ```

   Isso executa:

   1. `alembic stamp head`
   2. `alembic upgrade head`
   3. `python -m app.scripts.populate_db --number 100`
   4. `python -m app.mcp.server --host 0.0.0.0 --port 5000`

3. Para usar a CLI no host:

   ```bash
   python -m app.cli.main
   ```

   Ou dentro do container:

   ```bash
   docker-compose exec app python -m app.cli.main
   ```

4. Para rodar testes dentro do container:

   ```bash
   docker-compose exec app pytest
   ```

## 📦 Estrutura do Projeto

```
car_search/
├── .env.example
├── .env                # copiado e editado
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── migrations/
├── app/
│   ├── cli/
│   ├── mcp/
│   ├── models/
│   └── scripts/
└── tests/
```
