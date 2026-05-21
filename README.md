# Task Manager API

API REST para gerenciamento de tarefas com autenticação JWT, construída com FastAPI e PostgreSQL.

## Tecnologias

- **Python 3.14**
- **FastAPI** — framework web moderno e de alta performance
- **PostgreSQL** — banco de dados relacional
- **SQLAlchemy** — ORM para mapeamento objeto-relacional
- **Alembic** — migrações de banco de dados
- **python-jose** — geração e validação de tokens JWT
- **bcrypt** — hash seguro de senhas
- **Pydantic** — validação de dados e schemas
- **Uvicorn** — servidor ASGI

## Pré-requisitos

- Python 3.10+
- PostgreSQL rodando localmente

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/task-manager-api.git
cd task-manager-api
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente criando um arquivo `.env` na raiz:
```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/taskmanager
SECRET_KEY=sua-chave-secreta-aqui
```

5. Crie o banco de dados no PostgreSQL:
```sql
CREATE DATABASE taskmanager;
```

## Rodando o projeto

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`.

Documentação interativa (Swagger): `http://localhost:8000/docs`

## Endpoints

### Auth

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|:---:|
| POST | `/auth/login` | Login com email e senha | Não |

### Usuários

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|:---:|
| POST | `/users/` | Criar conta | Não |
| GET | `/users/me` | Dados do usuário logado | Sim |

### Tarefas

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|:---:|
| GET | `/tasks/` | Listar tarefas | Sim |
| POST | `/tasks/` | Criar tarefa | Sim |
| GET | `/tasks/{id}` | Buscar tarefa por ID | Sim |
| PUT | `/tasks/{id}` | Atualizar tarefa | Sim |
| DELETE | `/tasks/{id}` | Deletar tarefa | Sim |

> Endpoints marcados com **Sim** exigem o header `Authorization: Bearer <token>`.

## Exemplos de uso

### 1. Criar conta

```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "João Silva", "email": "joao@email.com", "password": "senha123"}'
```

**Resposta:**
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao@email.com",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00"
}
```

### 2. Fazer login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "joao@email.com", "password": "senha123"}'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Criar tarefa

```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Estudar FastAPI", "description": "Revisar documentação oficial"}'
```

**Resposta:**
```json
{
  "id": 1,
  "title": "Estudar FastAPI",
  "description": "Revisar documentação oficial",
  "completed": false,
  "created_at": "2024-01-15T10:35:00",
  "user_id": 1
}
```

### 4. Listar tarefas (com filtro opcional)

```bash
# Todas as tarefas
curl http://localhost:8000/tasks/ \
  -H "Authorization: Bearer <token>"

# Apenas pendentes
curl "http://localhost:8000/tasks/?completed=false" \
  -H "Authorization: Bearer <token>"

# Apenas concluídas
curl "http://localhost:8000/tasks/?completed=true" \
  -H "Authorization: Bearer <token>"
```

### 5. Atualizar tarefa

```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### 6. Deletar tarefa

```bash
curl -X DELETE http://localhost:8000/tasks/1 \
  -H "Authorization: Bearer <token>"
```

## Estrutura do projeto

```
task-manager-api/
├── app/
│   ├── dependencies.py     # Dependência get_current_user (JWT)
│   ├── models/
│   │   ├── user.py         # Modelo User
│   │   └── task.py         # Modelo Task
│   ├── routes/
│   │   ├── auth.py         # Rotas de autenticação
│   │   ├── users.py        # Rotas de usuários
│   │   └── tasks.py        # Rotas de tarefas
│   ├── schemas/
│   │   ├── user.py         # Schemas Pydantic de usuário
│   │   └── task.py         # Schemas Pydantic de tarefa
│   └── services/
│       └── auth.py         # JWT e hash de senha
├── database.py             # Configuração do SQLAlchemy
├── main.py                 # Entrypoint da aplicação
├── requirements.txt        # Dependências
└── .env                    # Variáveis de ambiente (não versionado)
```
