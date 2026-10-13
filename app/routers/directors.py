from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Director

router = APIRouter(prefix="/directors", tags=["directors"])

class DirectorCreate(BaseModel):
    fio: str
    position: str = ""
    company: str = ""
    bio: str = ""

class DirectorOut(DirectorCreate):
    id: int
    class Config:
        from_attributes = True

@router.get("/", response_model=list[DirectorOut])
def get_directors(db: Session = Depends(get_db)):
    return db.query(Director).all()

@router.post("/", response_model=DirectorOut)
def create_director(data: DirectorCreate, db: Session = Depends(get_db)):
    director = Director(**data.dict())
    db.add(director)
    db.commit()
    db.refresh(director)
    return director

@router.delete("/{director_id}")
def delete_director(director_id: int, db: Session = Depends(get_db)):
    obj = db.query(Director).filter(Director.id == director_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return {"status": "deleted"}