from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.domain.entities.usuario import Usuario
from app.core.security import verificar_senha
from fastapi import HTTPException

class UsuarioService:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def autenticar(self, email: str, senha: str) -> Usuario:
        model = self.repo.buscar_por_email(email)
        if not model or not verificar_senha(senha, model.senha_hash):
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
        return self.repo.to_entity(model)
