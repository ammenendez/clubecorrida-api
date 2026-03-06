from __future__ import annotations

import pytest
from app.domain.entities.clube import Clube
from app.domain.exceptions import DomainException


# ── helpers ───────────────────────────────────────────────────────────────────

CNPJ_VALIDO = "11222330001039"
CNPJ_DIGITOS_ERRADOS = "11222330001000"  # formato ok, dígitos verificadores errados
CNPJ_CURTO = "1234567"
CNPJ_COM_LETRAS = "1234567800019X"
CNPJ_SEQUENCIA = "00000000000000"  # todos iguais

DADOS_BASE = dict(
    cnpj=CNPJ_VALIDO,
    nome="Aracaju Runners",
    endereco="Av. Beira Mar, 123",
    cep="49020000",
    cidade="Aracaju",
    estado="SE",
)


def make_clube(**override) -> Clube:
    return Clube(**{**DADOS_BASE, **override})


# ── CNPJ ──────────────────────────────────────────────────────────────────────

def test_cnpj_curto_levanta_excecao():
    with pytest.raises(DomainException):
        make_clube(cnpj=CNPJ_CURTO)


def test_cnpj_com_letras_levanta_excecao():
    with pytest.raises(DomainException):
        make_clube(cnpj=CNPJ_COM_LETRAS)


def test_cnpj_sequencia_igual_levanta_excecao():
    with pytest.raises(DomainException):
        make_clube(cnpj=CNPJ_SEQUENCIA)


def test_cnpj_digitos_verificadores_errados_levanta_excecao():
    with pytest.raises(DomainException):
        make_clube(cnpj=CNPJ_DIGITOS_ERRADOS)


def test_cnpj_valido_aceito():
    clube = make_clube(cnpj=CNPJ_VALIDO)
    assert clube.cnpj == CNPJ_VALIDO


# ── Estado (UF) ───────────────────────────────────────────────────────────────

def test_estado_lowercase_levanta_excecao():
    with pytest.raises(DomainException):
        make_clube(estado="se")


def test_estado_tamanho_errado_levanta_excecao():
    with pytest.raises(DomainException):
        make_clube(estado="SER")


def test_estado_valido_aceito():
    clube = make_clube(estado="SE")
    assert clube.estado == "SE"


# ── CEP ───────────────────────────────────────────────────────────────────────

def test_cep_curto_levanta_excecao():
    with pytest.raises(DomainException):
        make_clube(cep="4902")


def test_cep_com_mascara_valido():
    clube = make_clube(cep="49020-000")
    assert clube.cep == "49020-000"


def test_cep_sem_mascara_valido():
    clube = make_clube(cep="49020000")
    assert clube.cep == "49020000"


# ── Clube completo ────────────────────────────────────────────────────────────

def test_clube_completo_valido():
    clube = make_clube()
    assert clube.cnpj == CNPJ_VALIDO
    assert clube.cidade == "Aracaju"
    assert clube.id is None  # id começa sem valor


def test_clube_com_id():
    clube = make_clube(id=42)
    assert clube.id == 42
