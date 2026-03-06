from sqlalchemy.orm import Session
from app.infrastructure.database.models import UsuarioModel
from app.domain.entities.usuario import Usuario, Role

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_email(self, email: str) -> UsuarioModel | None:
        return self.db.query(UsuarioModel).filter_by(email=email).first()

    def to_entity(self, model: UsuarioModel) -> Usuario:
        return Usuario(
            id=model.id,
            nome=model.nome,
            email=model.email,
            senha_hash=model.senha_hash,
            role=model.role,
            clube_id=model.clube_id,
        )
