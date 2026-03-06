from __future__ import annotations

from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.infrastructure.database.models import ClubeModel
from app.domain.entities.clube import Clube


class ClubeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, clube_data: Dict[str, Any]) -> Clube:
        clube_data = dict(clube_data)
        clube_data.pop("id", None)

        db_clube = ClubeModel(**clube_data)
        try:
            self.db.add(db_clube)
            self.db.commit()
            self.db.refresh(db_clube)
        except IntegrityError:
            self.db.rollback()
            raise
        return self._to_entity(db_clube)

    def get_by_id(self, clube_id: int) -> Optional[Clube]:
        db_clube = (
            self.db.query(ClubeModel)
            .filter(ClubeModel.id == clube_id)
            .first()
        )
        return self._to_entity(db_clube) if db_clube else None

    def get_by_cnpj(self, cnpj: str) -> Optional[Clube]:
        db_clube = (
            self.db.query(ClubeModel)
            .filter(ClubeModel.cnpj == cnpj)
            .first()
        )
        return self._to_entity(db_clube) if db_clube else None

    def list_all(self) -> List[Clube]:
        db_clubes = self.db.query(ClubeModel).all()
        return [self._to_entity(c) for c in db_clubes]

    def update(self, clube_id: int, dados_update: Dict[str, Any]) -> Optional[Clube]:
        db_clube = (
            self.db.query(ClubeModel)
            .filter(ClubeModel.id == clube_id)
            .first()
        )
        if not db_clube:
            return None

        # whitelist: só estes campos podem ser alterados
        allowed = {"nome", "endereco", "cep", "cidade", "estado"}
        dados_update = {k: v for k, v in dados_update.items() if k in allowed}

        if not dados_update:
            return self._to_entity(db_clube)

        for campo, valor in dados_update.items():
            setattr(db_clube, campo, valor)

        try:
            self.db.commit()
            self.db.refresh(db_clube)
        except IntegrityError:
            self.db.rollback()
            raise

        return self._to_entity(db_clube)

    def delete(self, clube_id: int) -> bool:
        db_clube = (
            self.db.query(ClubeModel)
            .filter(ClubeModel.id == clube_id)
            .first()
        )
        if not db_clube:
            return False

        try:
            self.db.delete(db_clube)
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise

        return True

    def _to_entity(self, db_clube: ClubeModel) -> Clube:
        return Clube(
            cnpj=db_clube.cnpj,
            nome=db_clube.nome,
            endereco=db_clube.endereco,
            cep=db_clube.cep,
            cidade=db_clube.cidade,
            estado=db_clube.estado,
            id=db_clube.id,  # id por último (dataclass)
        )
