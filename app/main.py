from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine, get_db
from . import models, schemas
from .agenda import create_meeting_with_agenda
from .voting import vote, get_results
from .protocol import generate_protocol

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# СНАЧАЛА создаем app
app = FastAPI(title="Совет Директоров")

# ПОТОМ уже добавляем middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/directors/")
def add_director(d: schemas.DirectorCreate, db: Session = Depends(get_db)):
    obj = models.Director(**d.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/directors/")
def list_directors(db: Session = Depends(get_db)):
    return db.query(models.Director).all()

@app.post("/meetings/")
def create_meeting(m: schemas.MeetingCreate, db: Session = Depends(get_db)):
    return create_meeting_with_agenda(db, m)

@app.get("/meetings/")
def list_meetings(db: Session = Depends(get_db)):
    return db.query(models.Meeting).all()

@app.post("/vote/")
def do_vote(v: schemas.VoteCreate, db: Session = Depends(get_db)):
    return vote(db, v.agenda_item_id, v.director_id, v.choice, v.ecp_signature)

@app.get("/results/{agenda_item_id}")
def results(agenda_item_id: int, db: Session = Depends(get_db)):
    return get_results(db, agenda_item_id)

@app.get("/protocol/{meeting_id}")
def protocol(meeting_id: int, db: Session = Depends(get_db)):
    return {"protocol": generate_protocol(db, meeting_id)}

@app.get("/")
def root():
    return {"status": "API работает"}