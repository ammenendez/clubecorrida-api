from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.usuario_repository import UsuarioRepository
from app.application.services.usuario_service import UsuarioService
from app.core.security import decodificar_token
from app.domain.entities.usuario import Usuario, Role
from app.infrastructure.repositories.clube_repository import ClubeRepository
from app.application.services.clube_service import ClubeService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_usuario_service(db: Session = Depends(get_db)) -> UsuarioService:
    return UsuarioService(UsuarioRepository(db))


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    try:
        payload = decodificar_token(token)
        repo = UsuarioRepository(db)
        model = repo.buscar_por_email(payload["sub"])
        if not model:
            raise Exception()
        return repo.to_entity(model)
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")


def require_admin_sistema(user: Usuario = Depends(get_current_user)) -> Usuario:
    if user.role != Role.ADMIN_SISTEMA:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user


def require_admin_clube(user: Usuario = Depends(get_current_user)) -> Usuario:
    if user.role not in (Role.ADMIN_SISTEMA, Role.ADMIN_CLUBE):
        raise HTTPException(status_code=403, detail="Acesso negado")
    return user


def get_clube_repo(db: Session = Depends(get_db)):
    return ClubeRepository(db)


def get_clube_service(repo=Depends(get_clube_repo)):
    return ClubeService(repo)
