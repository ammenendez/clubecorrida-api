from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class ClubeCreateDTO(BaseModel):
    cnpj: str = Field(..., min_length=14, max_length=14)
    nome: str = Field(..., max_length=120)
    endereco: str = Field(..., max_length=255)
    cep: str = Field(..., min_length=8, max_length=9)
    cidade: str = Field(..., max_length=80)
    estado: str = Field(..., pattern=r"^[A-Z]{2}$")  # era regex

class ClubeUpdateDTO(BaseModel):
    nome: Optional[str] = Field(None, max_length=120)
    endereco: Optional[str] = Field(None, max_length=255)
    cep: Optional[str] = Field(None, min_length=8, max_length=9)
    cidade: Optional[str] = Field(None, max_length=80)
    estado: Optional[str] = Field(None, pattern=r"^[A-Z]{2}$")  # era regex

class ClubeDTO(ClubeCreateDTO):
    id: int

    model_config = {"from_attributes": True}
