from __future__ import annotations

import pytest


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def payload():
    return {
        "cnpj": "11222330001039",
        "nome": "Aracaju Runners",
        "endereco": "Av. Beira Mar, 123",
        "cep": "49020000",
        "cidade": "Aracaju",
        "estado": "SE",
    }


@pytest.fixture
def clube_criado(client, payload):
    """Cria um clube e retorna o JSON de resposta — reutilizável nos testes."""
    r = client.post("/api/v1/clubes/", json=payload)
    assert r.status_code == 201
    return r.json()


# ── POST /clubes/ ─────────────────────────────────────────────────────────────

def test_criar_clube_sucesso(client, payload):
    r = client.post("/api/v1/clubes/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["cnpj"] == payload["cnpj"]
    assert data["nome"] == payload["nome"]
    assert "id" in data


def test_criar_clube_cnpj_duplicado(client, clube_criado, payload):
    r = client.post("/api/v1/clubes/", json=payload)
    assert r.status_code == 409
    assert "CNPJ" in r.json()["detail"]


def test_criar_clube_payload_invalido(client):
    r = client.post("/api/v1/clubes/", json={"cnpj": "123"})
    assert r.status_code == 422


def test_criar_clube_estado_lowercase(client, payload):
    payload["estado"] = "se"
    r = client.post("/api/v1/clubes/", json=payload)
    assert r.status_code == 422


def test_criar_clube_cnpj_curto(client, payload):
    payload["cnpj"] = "123"
    r = client.post("/api/v1/clubes/", json=payload)
    assert r.status_code == 422


# ── GET /clubes/{id} ──────────────────────────────────────────────────────────

def test_obter_clube_sucesso(client, clube_criado):
    clube_id = clube_criado["id"]
    r = client.get(f"/api/v1/clubes/{clube_id}")
    assert r.status_code == 200
    assert r.json()["id"] == clube_id


def test_obter_clube_inexistente(client):
    r = client.get("/api/v1/clubes/999999")
    assert r.status_code == 404


# ── GET /clubes/ ──────────────────────────────────────────────────────────────

def test_listar_clubes_retorna_lista(client, clube_criado):
    r = client.get("/api/v1/clubes/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    ids = [c["id"] for c in r.json()]
    assert clube_criado["id"] in ids


def test_listar_clubes_retorna_lista_vazia(client):
    r = client.get("/api/v1/clubes/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


# ── PATCH /clubes/{id} ────────────────────────────────────────────────────────

def test_atualizar_clube_sucesso(client, clube_criado):
    clube_id = clube_criado["id"]
    r = client.patch(f"/api/v1/clubes/{clube_id}", json={"nome": "Novo Nome"})
    assert r.status_code == 200
    assert r.json()["nome"] == "Novo Nome"


def test_atualizar_clube_inexistente(client):
    r = client.patch("/api/v1/clubes/999999", json={"nome": "X"})
    assert r.status_code == 404


def test_atualizar_clube_estado_invalido(client, clube_criado):
    clube_id = clube_criado["id"]
    r = client.patch(f"/api/v1/clubes/{clube_id}", json={"estado": "sp"})
    assert r.status_code == 422


def test_atualizar_clube_sem_campos(client, clube_criado):
    """PATCH com body vazio deve retornar o clube sem alterações."""
    clube_id = clube_criado["id"]
    r = client.patch(f"/api/v1/clubes/{clube_id}", json={})
    assert r.status_code == 200
    assert r.json()["id"] == clube_id


# ── DELETE /clubes/{id} ───────────────────────────────────────────────────────

def test_deletar_clube_sucesso(client, clube_criado):
    clube_id = clube_criado["id"]
    r = client.delete(f"/api/v1/clubes/{clube_id}")
    assert r.status_code == 204


def test_deletar_clube_inexistente(client):
    r = client.delete("/api/v1/clubes/999999")
    assert r.status_code == 404


def test_deletar_clube_some_do_banco(client, clube_criado):
    clube_id = clube_criado["id"]
    client.delete(f"/api/v1/clubes/{clube_id}")
    r = client.get(f"/api/v1/clubes/{clube_id}")
    assert r.status_code == 404
