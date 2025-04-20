from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Conexão com banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schemas
class TarefaCreate(BaseModel):
    titulo: str
    prazo: datetime

class TarefaShow(BaseModel):
    id: int
    titulo: str
    prazo: datetime
    concluida: bool

    class Config:
        orm_mode = True

# Rotas
@app.get("/")
def home():
    return {"mensagem": "Bem-vindo ao Gerenciador de Tarefas!"}

@app.post("/tarefas", response_model=TarefaShow)
def criar_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    db_tarefa = models.Tarefa(titulo=tarefa.titulo, prazo=tarefa.prazo)
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

@app.get("/tarefas", response_model=List[TarefaShow])
def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(models.Tarefa).all()

@app.put("/tarefas/{tarefa_id}/concluir")
def concluir_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefa.concluida = True
    db.commit()
    return {"mensagem": "Tarefa marcada como concluída"}

@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(tarefa)
    db.commit()
    return {"mensagem": "Tarefa deletada"}
