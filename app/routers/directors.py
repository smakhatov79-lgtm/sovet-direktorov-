from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Director
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/directors", tags=["directors"])

class DirectorCreate(BaseModel):
    fio: Optional[str] = None
    name: Optional[str] = None
    full_name: Optional[str] = None
    position: Optional[str] = None
    role: Optional[str] = None
    company: Optional[str] = None
    bio: Optional[str] = None
    class Config:
        extra = "allow"

@router.get("/")
def list_directors(db: Session = Depends(get_db)):
    return db.query(Director).all()

@router.post("/")
def create_director(data: DirectorCreate, db: Session = Depends(get_db)):
    final_fio = data.fio or data.name or data.full_name or "Без имени"
    d = Director(fio=final_fio, position=data.position or data.role, company=data.company, bio=data.bio)
    db.add(d); db.commit(); db.refresh(d)
    return d

@router.delete("/{director_id}")
def delete_director(director_id: int, db: Session = Depends(get_db)):
    obj = db.query(Director).filter(Director.id == director_id).first()
    if obj:
        db.delete(obj); db.commit()
    return {"status": "deleted"}