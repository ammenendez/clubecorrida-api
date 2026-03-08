from typing import List
from typing import Optional 
from app.domain.entities.clube import Clube
from app.domain.exceptions import CnpjJaExisteException 
from app.infrastructure.repositories.clube_repository import ClubeRepository

class ClubeService:
    def __init__(self, repo: ClubeRepository):
        self.repo = repo

    def criar_clube(self, **dados) -> Clube:  # Aceita **kwargs
        cnpj = dados['cnpj']
        if self.repo.get_by_cnpj(cnpj):
            raise CnpjJaExisteException("CNPJ já cadastrado")
        return self.repo.create(dados)



    def obter_clube(self, clube_id: int) -> Clube | None:
        return self.repo.get_by_id(clube_id)

    def listar_clubes(self) -> List[Clube]:
        return self.repo.list_all()
    
    def atualizar_clube(self, clube_id: int, dados_update: dict) -> Optional[Clube]:
        if self.obter_clube(clube_id) is None:
            raise ValueError("Clube não encontrado")
        
        clube_atualizado = self.repo.update(clube_id, dados_update)
        return clube_atualizado

    def deletar_clube(self, clube_id: int) -> bool:
        return self.repo.delete(clube_id)

