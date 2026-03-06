from dataclasses import dataclass
from typing import Optional
from app.domain.exceptions import DomainException


@dataclass
class Clube:
    cnpj: str
    nome: str
    endereco: str
    cep: str
    cidade: str
    estado: str
    id: Optional[int] = None   # campo opcional DEPOIS dos obrigatórios

    def __post_init__(self):
            if not self._cnpj_valido(self.cnpj):
                raise DomainException("CNPJ inválido")
            if len(self.estado) != 2 or not self.estado.isupper():
                raise DomainException("Estado: 2 letras maiúsculas (UF)")
            if len(self.cep.replace("-", "")) != 8:
                raise DomainException("CEP inválido")

    @staticmethod
    def _cnpj_valido(cnpj: str) -> bool:
        if len(cnpj) != 14 or not cnpj.isdigit():
            return False
        if len(set(cnpj)) == 1:  # ex: "00000000000000"
            return False

        def calcular_digito(cnpj: str, pesos: list[int]) -> int:
            soma = sum(int(d) * p for d, p in zip(cnpj, pesos))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto

        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        d1 = calcular_digito(cnpj[:12], pesos1)
        d2 = calcular_digito(cnpj[:13], pesos2)

        return cnpj[-2:] == f"{d1}{d2}"
