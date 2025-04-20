from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base

class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    prazo = Column(DateTime)
    concluida = Column(Boolean, default=False)
