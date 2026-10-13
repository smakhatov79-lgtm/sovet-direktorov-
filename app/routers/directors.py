from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Director
from app.schemas import DirectorCreate, DirectorOut
from typing import List

router = APIRouter(prefix="/directors", tags=["directors"])

@router.get("/", response_model=List[DirectorOut])
def list_directors(db: Session = Depends(get_db)):
    return db.query(Director).all()

@router.post("/", response_model=DirectorOut)
def create_director(data: DirectorCreate, db: Session = Depends(get_db)):
    # проверка ИИН на уникальность
    exists = db.query(Director).filter(Director.iin == data.iin).first()
    if exists:
        raise HTTPException(status_code=400, detail="ИИН уже существует")

    d = Director(
        last_name=data.last_name,
        first_name=data.first_name,
        middle_name=data.middle_name,
        iin=data.iin,
        birth_date=data.birth_date,
        position=data.position,
        status=data.status
    )
    db.add(d)
    db.commit()
    db.refresh(d)
    return d

@router.delete("/{director_id}")
def delete_director(director_id: int, db: Session = Depends(get_db)):
    obj = db.query(Director).filter(Director.id == director_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}