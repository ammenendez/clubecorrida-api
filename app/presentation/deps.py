from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.clube_repository import ClubeRepository
from app.application.services.clube_service import ClubeService

def get_clube_repo(db: Session = Depends(get_db)):
    return ClubeRepository(db)

def get_clube_service(repo = Depends(get_clube_repo)):
    return ClubeService(repo)
