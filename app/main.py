from fastapi import FastAPI
from app.infrastructure.database import Base, engine
from app.presentation.api.v1 import clubes

# Cria tabelas na inicialização
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clube da Corrida API")

app.include_router(clubes.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Clube da Corrida API - Pronto para CRUD!"}


@app.get("/health")
def health():
    return {"status": "ok"}

