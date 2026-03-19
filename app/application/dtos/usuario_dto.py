from pydantic import BaseModel

class LoginResponseDTO(BaseModel):
    access_token: str
    token_type: str
    nome: str
    role: str
    clube_id: int | None