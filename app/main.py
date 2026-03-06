from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.database import Base, engine
from app.presentation.api.v1 import clubes, auth

# Cria tabelas na inicialização
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clube da Corrida API")

# --- CORS ---
origins = [
    "http://localhost:3000",   # frontend local (React, Vue, etc.)
    "http://localhost:5173",   # Vite
    # "https://meudominio.com" # produção
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------

app.include_router(clubes.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Clube da Corrida API - Pronto para CRUD!"}


@app.get("/health")
def health():
    return {"status": "ok"}
