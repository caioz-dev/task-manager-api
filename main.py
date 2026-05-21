from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.dirname(__file__))
from database import engine, Base
from app.models import user, task
from app.routes import users, auth, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="API de gerenciamento de tarefas com autenticação JWT",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Task Manager API funcionando!"}