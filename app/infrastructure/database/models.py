from sqlalchemy import Column, Integer, String
from .session import Base

class ClubeModel(Base):
    __tablename__ = "clubes"

    id = Column(Integer, primary_key=True, index=True)
    cnpj = Column(String(14), unique=True, index=True, nullable=False)
    nome = Column(String(120), nullable=False)
    endereco = Column(String(255), nullable=False)
    cep = Column(String(8), nullable=False)
    cidade = Column(String(80), nullable=False)
    estado = Column(String(2), nullable=False)
