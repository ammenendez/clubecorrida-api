from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dtos.clube_dto import ClubeCreateDTO, ClubeDTO, ClubeUpdateDTO
from app.application.services.clube_service import ClubeService
from app.domain.entities.usuario import Usuario
from app.domain.exceptions import CnpjJaExisteException, DomainException
from app.presentation.deps import get_clube_service, get_current_user, require_admin_sistema


router = APIRouter(prefix="/clubes", tags=["Clubes"])


@router.post("/", response_model=ClubeDTO, status_code=status.HTTP_201_CREATED)
def criar_clube(
    clube_dto: ClubeCreateDTO,
    service: ClubeService = Depends(get_clube_service),
    _: Usuario = Depends(require_admin_sistema),
):
    try:
        clube = service.criar_clube(**clube_dto.model_dump())
        return clube
    except CnpjJaExisteException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get("/", response_model=list[ClubeDTO])
def listar_clubes(
    service: ClubeService = Depends(get_clube_service),
    _: Usuario = Depends(get_current_user),
):
    return service.listar_clubes()


@router.get("/{clube_id}", response_model=ClubeDTO)
def obter_clube(
    clube_id: int,
    service: ClubeService = Depends(get_clube_service),
    _: Usuario = Depends(get_current_user),
):
    clube = service.obter_clube(clube_id)
    if not clube:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clube não encontrado")
    return clube


@router.patch("/{clube_id}", response_model=ClubeDTO)
def atualizar_clube(
    clube_id: int,
    dados_update: ClubeUpdateDTO,
    service: ClubeService = Depends(get_clube_service),
    _: Usuario = Depends(require_admin_sistema),
):
    try:
        update_data = dados_update.model_dump(exclude_unset=True)
        clube = service.atualizar_clube(clube_id, update_data)
        if not clube:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clube não encontrado")
        return clube
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.delete("/{clube_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_clube(
    clube_id: int,
    service: ClubeService = Depends(get_clube_service),
    _: Usuario = Depends(require_admin_sistema),
):
    ok = service.deletar_clube(clube_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clube não encontrado")
