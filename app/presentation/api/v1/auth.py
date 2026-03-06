from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.application.services.usuario_service import UsuarioService
from app.presentation.deps import get_usuario_service
from app.core.security import criar_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    service: UsuarioService = Depends(get_usuario_service),
):
    user = service.autenticar(form.username, form.password)
    token = criar_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
