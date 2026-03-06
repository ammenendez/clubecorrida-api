# app/domain/entities/usuario.py
from dataclasses import dataclass
from enum import Enum

class Role(str, Enum):
    ADMIN_SISTEMA = "admin_sistema"
    ADMIN_CLUBE   = "admin_clube"
    ATLETA        = "atleta"

@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    senha_hash: str
    role: Role
    clube_id: int | None = None  # obrigatório para admin_clube e atleta
