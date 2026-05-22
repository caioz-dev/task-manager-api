# Task Manager API

API REST para gerenciamento de tarefas com autenticação JWT, construída com FastAPI e PostgreSQL.

## Stack

- **Python 3.14** + **FastAPI**
- **PostgreSQL 15** com **SQLAlchemy** (ORM) e **Alembic** (migrações)
- **JWT** via `python-jose`, senhas com `bcrypt`
- **Pydantic** para validação de schemas
- **Uvicorn** como servidor ASGI
- **Docker** + **docker-compose** para ambiente containerizado

## Estrutura do projeto

```
task-manager-api/
├── app/
│   ├── dependencies.py     # Dependência get_current_user (JWT)
│   ├── models/
│   │   ├── user.py         # Modelo User (SQLAlchemy)
│   │   └── task.py         # Modelo Task (SQLAlchemy)
│   ├── routes/
│   │   ├── auth.py         # POST /auth/login
│   │   ├── users.py        # POST /users/, GET /users/me
│   │   └── tasks.py        # CRUD /tasks/
│   ├── schemas/
│   │   ├── user.py         # Schemas Pydantic de usuário
│   │   └── task.py         # Schemas Pydantic de tarefa
│   └── services/
│       └── auth.py         # Geração/validação de JWT e hash de senha
├── database.py             # Configuração do SQLAlchemy (engine, SessionLocal, Base)
├── main.py                 # Entrypoint — registra routers e cria tabelas
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env                    # Não versionado — ver .env.example
```

## Variáveis de ambiente

Crie um arquivo `.env` na raiz baseado no `.env.example`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/taskmanager
SECRET_KEY=sua-chave-secreta-aqui
```

## Como rodar

### Localmente

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Com Docker

```bash
docker-compose up --build          # sobe api + db
docker-compose up --build -d       # em background
docker-compose down                # para os containers
docker-compose down -v             # para e apaga volume do banco
```

A API sobe em `http://localhost:8000`. Swagger UI: `http://localhost:8000/docs`.

## Endpoints

### Auth
| Método | Rota | Auth |
|--------|------|:----:|
| POST | `/auth/login` | Não |

### Usuários
| Método | Rota | Auth |
|--------|------|:----:|
| POST | `/users/` | Não |
| GET | `/users/me` | Sim |

### Tarefas
| Método | Rota | Auth |
|--------|------|:----:|
| GET | `/tasks/` | Sim |
| POST | `/tasks/` | Sim |
| GET | `/tasks/{id}` | Sim |
| PUT | `/tasks/{id}` | Sim |
| DELETE | `/tasks/{id}` | Sim |

Endpoints autenticados exigem header `Authorization: Bearer <token>`.

O endpoint `GET /tasks/` aceita query param `?completed=true/false` para filtrar tarefas.

## Banco de dados

### Tabela `users`
| Coluna | Tipo | Observação |
|--------|------|------------|
| id | integer PK | auto-incremento |
| name | varchar(100) | obrigatório |
| email | varchar(150) | único, obrigatório |
| password | varchar(255) | hash bcrypt |
| is_active | boolean | |
| created_at | timestamp | |

### Tabela `tasks`
| Coluna | Tipo | Observação |
|--------|------|------------|
| id | integer PK | auto-incremento |
| title | varchar(100) | obrigatório |
| description | varchar(500) | opcional |
| completed | boolean | |
| created_at | timestamp | |
| user_id | integer FK | referencia users(id) |

## Padrões do projeto

- Cada domínio tem seu próprio módulo em `models/`, `schemas/` e `routes/`
- A dependência `get_current_user` em `app/dependencies.py` é usada em todos os endpoints protegidos
- Autenticação via JWT — o token é gerado no login e validado a cada requisição protegida
- As tabelas são criadas automaticamente pelo SQLAlchemy no startup (`main.py`) — sem Alembic em desenvolvimento

## Checklist para novos endpoints

Ao criar um novo endpoint, as seguintes etapas são obrigatórias:

1. **Schema Pydantic** — criar ou atualizar o schema correspondente em `app/schemas/` (request body, response model e eventuais schemas intermediários)
2. **Testes unitários** — criar testes para o novo endpoint em `tests/`, cobrindo o caso de sucesso e os principais casos de erro (ex: não autenticado, recurso não encontrado, dados inválidos)
3. **README** — atualizar a tabela de endpoints em `README.md` com o novo método, rota, descrição e se exige autenticação
