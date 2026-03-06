# ClubeCorrida API

API em FastAPI organizada com **Clean Architecture**, persistência com **SQLAlchemy + MySQL**, e testes com **pytest** (unit + API/integration) usando banco de teste (`clubecorrida_test`).

## Sumário

- [Visão geral](#visão-geral)
- [Clean Architecture no projeto](#clean-architecture-no-projeto)
- [Estrutura de pastas](#estrutura-de-pastas)
- [Fluxo de uma requisição (ex: POST /clubes)](#fluxo-de-uma-requisição-ex-post-clubes)
- [Regras de dependência (o que pode importar o quê)](#regras-de-dependência-o-que-pode-importar-o-quê)
- [Rodando o projeto](#rodando-o-projeto)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Testes](#testes)
- [Migrations com Alembic](#migrations-com-alembic)
- [Como adicionar um atributo em uma entidade existente](#como-adicionar-um-atributo-em-uma-entidade-existente)
- [Como criar uma nova entidade (checklist)](#como-criar-uma-nova-entidade-checklist)
- [Padrões e decisões](#padrões-e-decisões)
- [Troubleshooting](#troubleshooting)

---

## Visão geral

A API implementa endpoints para **Clubes** (criar, listar, buscar por id, atualizar e deletar), seguindo princípios de **Clean Architecture** para isolar regras de negócio de detalhes de framework e banco.

Objetivos principais:
- Separar regras do negócio (domínio) de detalhes externos (FastAPI, SQLAlchemy, MySQL).
- Facilitar testes: unitários no domínio e testes de API integrados com banco de teste.
- Permitir evolução (novas entidades) sem acoplamento ao framework.

---

## Clean Architecture no projeto

Clean Architecture organiza o software em camadas concêntricas. A regra essencial é:

**Dependency Rule**: dependências do código devem apontar sempre para dentro.
Ou seja, camadas externas **podem depender** das internas, mas as internas **não** devem depender das externas.

No nosso projeto:
- O **Domínio** não conhece FastAPI, SQLAlchemy, MySQL, DTO, Request/Response etc.
- A **Application** orquestra casos de uso (services) e usa repositórios para persistir.
- A **Infrastructure** implementa banco e repositórios concretos (SQLAlchemy).
- A **Presentation** (API) recebe HTTP e chama a Application.

---

## Estrutura de pastas

Estrutura principal (resumo):

```text
app/
  main.py
  core/
    config.py
  domain/
    entities/
    exceptions.py
  application/
    dtos/
    services/
  infrastructure/
    database/
      session.py
      models.py
    repositories/
  presentation/
    deps.py
    api/
      v1/
tests/
  conftest.py
  api/
  unit/
```

### O que vai em cada camada?

#### `app/domain/` (Domínio)
- Entidades (ex: `Clube`)
- Regras e validações do negócio (invariantes)
- Exceções de domínio (`DomainException` etc.)

> Não deve importar nada de FastAPI/SQLAlchemy.

#### `app/application/` (Casos de uso / Application Services)
- `services/`: coordena o fluxo do caso de uso (ex: criar clube, atualizar clube etc.)
- `dtos/`: contratos de entrada/saída (o que a API recebe/devolve)

Aqui você coloca regras do fluxo (ex: "CNPJ não pode duplicar"), mas sem detalhes do banco.

#### `app/infrastructure/` (Infra)
- `database/models.py`: modelos ORM do SQLAlchemy
- `database/session.py`: engine, sessão e dependência `get_db`
- `repositories/`: implementação concreta dos repositórios (CRUD no MySQL)

Aqui mora o "mundo real": SQLAlchemy, MySQL, commits, rollback, IntegrityError etc.

#### `app/presentation/` (Entrada/Interface)
- Rotas FastAPI (`api/v1/clubes.py`)
- `deps.py`: injeção de dependências (ex: instanciar service com repository + session)

Responsável por:
- Ler request
- Validar via DTO (Pydantic)
- Chamar service
- Converter erros para HTTP (ex: 404, 400, 409 etc.)

#### `app/main.py` (Composição)
Ponto de composição do app:
- Cria instância `FastAPI()`
- Registra routers
- Middlewares e configurações globais

---

## Fluxo de uma requisição (ex: POST /clubes)

1. HTTP chega no router: `app/presentation/api/v1/clubes.py`
2. Router valida body via DTO (`app/application/dtos/*`)
3. Router injeta dependências via `deps.py` e chama `ClubeService`
4. `ClubeService` aplica regra de caso de uso (ex: verificar duplicidade)
5. Service chama o repositório (infra) para persistir no MySQL
6. Repository usa ORM + Session (`infrastructure/database`) e retorna entidade do domínio
7. Router devolve response + status code correto

---

## Regras de dependência (o que pode importar o quê)

Regra prática para manter o projeto saudável:

- `domain` **não importa** nada de `application`, `infrastructure`, `presentation`
- `application` pode importar `domain`
- `infrastructure` pode importar `domain`
- `presentation` pode importar `application` e `infrastructure` (para wiring/deps)
- `main.py` pode importar todos (é a composição)

Se você perceber `domain` importando `sqlalchemy` ou `fastapi`, é um sinal de acoplamento indevido.

---

## Rodando o projeto

### Requisitos
- Python 3.x
- MySQL rodando localmente
- Virtualenv recomendado

### Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Rodar API

```bash
uvicorn app.main:app --reload
```

Docs:
- Swagger: http://127.0.0.1:8000/docs
- OpenAPI: http://127.0.0.1:8000/openapi.json

---

## Variáveis de ambiente

### `.env` (desenvolvimento)

```env
DATABASE_URL=mysql+mysqlconnector://root:SENHA@localhost:3306/clubecorrida
```

### `.env.test` (testes)

```env
DATABASE_URL=mysql+mysqlconnector://root:SENHA@localhost:3306/clubecorrida_test
```

Recomendação: use sempre um schema separado de testes para evitar "sujar" o banco de dev.

---

## Testes

### Estratégia
- **Unit tests**: validam regras de domínio e services sem infraestrutura pesada.
- **API tests**: validam endpoints com `TestClient` e MySQL de teste, usando override da dependência `get_db` (via `app.dependency_overrides`).

### Pré-requisito: schema de teste

Crie uma vez no MySQL:

```sql
CREATE DATABASE IF NOT EXISTS clubecorrida_test;
```

### Rodar testes

Tudo:

```bash
pytest -v
```

Rodar um arquivo:

```bash
pytest -v tests/api/test_clubes_endpoints.py
```

Rodar um teste específico:

```bash
pytest -v tests/api/test_clubes_endpoints.py::test_crud_clube
```

### Cobertura

Terminal:

```bash
pytest -v --cov=app --cov-report=term-missing
```

HTML:

```bash
pytest -v --cov=app --cov-report=html
# abre htmlcov/index.html
```

### Importante (para segurança)

No `tests/conftest.py`, carregue `.env.test` com override e garanta que o app só é importado depois disso, para evitar rodar teste no banco de dev.

---

## Migrations com Alembic

O Alembic gerencia o versionamento do schema do banco. Ele compara os models SQLAlchemy (`Base.metadata`) com o estado atual do banco e gera o SQL necessário automaticamente via `--autogenerate`.

### Diferença entre os casos

| Situação | O que o Alembic detecta | SQL gerado |
|---|---|---|
| Nova entidade (`RunnerModel`) | Tabela existe no metadata mas não no banco | `CREATE TABLE runners (...)` |
| Novo atributo em entidade existente | Coluna existe no model mas não na tabela | `ALTER TABLE clubes ADD COLUMN telefone` |
| Nenhuma mudança | Tudo igual | Migration vazia |

### Pré-requisito: importar todos os models no `alembic/env.py`

Para o Alembic detectar os models via `--autogenerate`, todos devem estar importados antes do `run_migrations`:

```python
# alembic/env.py
from app.infrastructure.database.models import Base
from app.infrastructure.database import models  # noqa: garante que todos os models são carregados

target_metadata = Base.metadata
```

> Se você criar um novo model mas não importá-lo aqui, o Alembic não enxerga e não gera o `CREATE TABLE`. Esse é o erro mais comum.

### Comandos úteis

Criar uma nova migration (detecta mudanças automaticamente):

```bash
alembic revision --autogenerate -m "descricao da mudanca"
```

Aplicar todas as migrations pendentes:

```bash
alembic upgrade head
```

Ver o histórico de migrations:

```bash
alembic history
```

Reverter a última migration:

```bash
alembic downgrade -1
```

Ver qual migration está aplicada atualmente:

```bash
alembic current
```

> Sempre revise o arquivo gerado em `alembic/versions/` antes de aplicar, especialmente em produção. O `--autogenerate` não detecta 100% dos casos (ex: renomeação de colunas).

---

## Como adicionar um atributo em uma entidade existente

Exemplo: adicionar `telefone` à entidade `Clube`.

### 1. `app/domain/entities/clube.py`

```python
@dataclass
class Clube:
    id: int
    nome: str
    cnpj: str
    telefone: str | None = None  # novo
```

### 2. `app/infrastructure/database/models.py`

```python
class ClubeModel(Base):
    __tablename__ = "clubes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=False)
    telefone = Column(String(20), nullable=True)  # novo
```

### 3. `app/application/dtos/clube_dto.py`

```python
class ClubeCreateDTO(BaseModel):
    nome: str
    cnpj: str
    telefone: str | None = None  # novo

class ClubeResponseDTO(BaseModel):
    id: int
    nome: str
    cnpj: str
    telefone: str | None = None  # novo
```

### 4. `app/infrastructure/repositories/clube_repository.py`

```python
def _to_entity(self, model: ClubeModel) -> Clube:
    return Clube(
        id=model.id,
        nome=model.nome,
        cnpj=model.cnpj,
        telefone=model.telefone,  # novo
    )
```

### 5. Gerar e aplicar a migration

```bash
alembic revision --autogenerate -m "add telefone to clubes"
alembic upgrade head
```

---

## Como criar uma nova entidade (checklist)

Exemplo: criar entidade `Runner`.

1. **Domínio**
   - Criar `app/domain/entities/runner.py`
   - Definir regras/invariantes e exceções (se necessário)

2. **Infra (ORM)**
   - Criar/editar `app/infrastructure/database/models.py` com `RunnerModel`
   - Garantir relacionamento (FK) se existir (ex: `clube_id`)
   - Garantir import do novo model em `alembic/env.py`

3. **Repository**
   - Criar `app/infrastructure/repositories/runner_repository.py`
   - CRUD + mapeamento ORM → entidade do domínio

4. **DTOs**
   - Criar `app/application/dtos/runner_dto.py` (Create/Update/Response)

5. **Service**
   - Criar `app/application/services/runner_service.py`
   - Regras de caso de uso (ex: runner deve pertencer a clube existente)

6. **API (Presentation)**
   - Criar router `app/presentation/api/v1/runners.py`
   - Incluir no `main.py` via `include_router`
   - Ajustar `deps.py` para injeção do service/repo

7. **Migration**
   - Rodar `alembic revision --autogenerate -m "create runners table"`
   - Revisar o arquivo gerado em `alembic/versions/`
   - Rodar `alembic upgrade head`

8. **Testes**
   - Unit: domínio + service
   - API: CRUD completo com MySQL de teste

---

## Padrões e decisões

- **PATCH** para update parcial: envia só campos que quer alterar.
- **DELETE** retorna `204 No Content` quando deleta com sucesso.
- Erros devem ser traduzidos para HTTP no layer `presentation` (ex: 404 quando não encontrado), evitando 500 por exceções vazando.

---

## Troubleshooting

### "Tabelas não aparecem no clubecorrida_test"
- Verifique se `.env.test` está sendo usado de verdade (o erro clássico é o teste rodar com `.env`).
- No conftest, use `load_dotenv(".env.test", override=True)` e só depois importe o `app`.

### "Alembic não detecta novo model"
- Verifique se o novo model está importado em `alembic/env.py`.
- Rode `alembic revision --autogenerate` e veja se o `CREATE TABLE` aparece no arquivo gerado.

### "OpenAPI/Swagger 500"
- Geralmente é erro de schema/DTO (Pydantic) ou forward references; revise imports e tipos.
