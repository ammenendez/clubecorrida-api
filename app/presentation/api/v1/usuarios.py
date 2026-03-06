# app/presentation/api/v1/usuarios.py
router = APIRouter(prefix="/usuarios", tags=["Usuários"])

# ✅ Pública — qualquer um pode se cadastrar como atleta
@router.post("/", status_code=201)
def cadastrar_atleta(dto: AtletaCadastroDTO, service: UsuarioService = Depends(get_usuario_service)):
    return service.cadastrar_atleta(dto)

# 🔒 Somente admin_sistema cria outros admins
@router.post("/admin", status_code=201)
def criar_admin(
    dto: UsuarioCreateDTO,
    current_user: Usuario = Depends(require_admin_sistema),
    service: UsuarioService = Depends(get_usuario_service),
):
    return service.criar_usuario_admin(dto, criado_por=current_user)
