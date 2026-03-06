from __future__ import annotations

from unittest.mock import MagicMock
import pytest

from app.application.services.clube_service import ClubeService
from app.domain.entities.clube import Clube
from app.domain.exceptions import CnpjJaExisteException


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def repo():
    return MagicMock()


@pytest.fixture
def service(repo):
    return ClubeService(repo=repo)


@pytest.fixture
def clube_valido():
    return Clube(
        id=1,
        cnpj="11222330001039",
        nome="Aracaju Runners",
        endereco="Av. Beira Mar, 123",
        cep="49020000",
        cidade="Aracaju",
        estado="SE",
    )


# ── criar_clube ───────────────────────────────────────────────────────────────

def test_criar_clube_sucesso(service, repo, clube_valido):
    repo.get_by_cnpj.return_value = None
    repo.create.return_value = clube_valido

    resultado = service.criar_clube(
        cnpj="11222330001039",
        nome="Aracaju Runners",
        endereco="Av. Beira Mar, 123",
        cep="49020000",
        cidade="Aracaju",
        estado="SE",
    )

    repo.get_by_cnpj.assert_called_once_with("11222330001039")
    repo.create.assert_called_once()
    assert resultado.cnpj == "11222330001039"


def test_criar_clube_cnpj_duplicado(service, repo, clube_valido):
    repo.get_by_cnpj.return_value = clube_valido  # simula CNPJ já existente

    with pytest.raises(CnpjJaExisteException, match="CNPJ já cadastrado"):
        service.criar_clube(
            cnpj="11222330001039",
            nome="Outro Clube",
            endereco="Rua X",
            cep="49020000",
            cidade="Aracaju",
            estado="SE",
        )

    repo.create.assert_not_called()  # nunca deve chegar ao repo


# ── obter_clube ───────────────────────────────────────────────────────────────

def test_obter_clube_existente(service, repo, clube_valido):
    repo.get_by_id.return_value = clube_valido

    resultado = service.obter_clube(1)

    repo.get_by_id.assert_called_once_with(1)
    assert resultado.id == 1


def test_obter_clube_inexistente(service, repo):
    repo.get_by_id.return_value = None

    resultado = service.obter_clube(999)

    assert resultado is None


# ── listar_clubes ─────────────────────────────────────────────────────────────

def test_listar_clubes_retorna_lista(service, repo, clube_valido):
    repo.list_all.return_value = [clube_valido, clube_valido]

    resultado = service.listar_clubes()

    assert len(resultado) == 2


def test_listar_clubes_vazio(service, repo):
    repo.list_all.return_value = []

    resultado = service.listar_clubes()

    assert resultado == []


# ── atualizar_clube ───────────────────────────────────────────────────────────

def test_atualizar_clube_sucesso(service, repo, clube_valido):
    repo.get_by_id.return_value = clube_valido
    clube_atualizado = Clube(
        id=1,
        cnpj="11222330001039",
        nome="Aracaju Runners 2",
        endereco="Av. Beira Mar, 123",
        cep="49020000",
        cidade="Aracaju",
        estado="SE",
    )
    repo.update.return_value = clube_atualizado

    resultado = service.atualizar_clube(1, {"nome": "Aracaju Runners 2"})

    repo.update.assert_called_once_with(1, {"nome": "Aracaju Runners 2"})
    assert resultado.nome == "Aracaju Runners 2"


def test_atualizar_clube_inexistente(service, repo):
    repo.get_by_id.return_value = None

    with pytest.raises(ValueError, match="Clube não encontrado"):
        service.atualizar_clube(999, {"nome": "X"})

    repo.update.assert_not_called()


# ── deletar_clube ─────────────────────────────────────────────────────────────

def test_deletar_clube_sucesso(service, repo):
    repo.delete.return_value = True

    resultado = service.deletar_clube(1)

    repo.delete.assert_called_once_with(1)
    assert resultado is True


def test_deletar_clube_inexistente(service, repo):
    repo.delete.return_value = False

    resultado = service.deletar_clube(999)

    assert resultado is False
