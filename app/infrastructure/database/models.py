from sqlalchemy import Column, Integer, String
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from app.domain.entities.usuario import Role
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


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id        = Column(Integer, primary_key=True, autoincrement=True)
    nome      = Column(String(100), nullable=False)
    email     = Column(String(150), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    role      = Column(Enum(Role), nullable=False, default=Role.ATLETA)
    clube_id  = Column(Integer, ForeignKey("clubes.id"), nullable=True)
