import os

os.makedirs("app", exist_ok=True)

# requirements.txt
open("requirements.txt","w").write("fastapi\nuvicorn\nsqlalchemy\npydantic\npython-multipart\n")

# app/__init__.py
open("app/__init__.py","w").write("")

# app/database.py
open("app/database.py","w", encoding="utf-8").write('''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
engine = create_engine("sqlite:///./board.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''')

# app/models.py
open("app/models.py","w", encoding="utf-8").write('''
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from.database import Base
import datetime

class Director(Base):
    __tablename__ = "directors"
    id = Column(Integer, primary_key=True)
    fio = Column(String(200), nullable=False)
    birth_date = Column(String(20))
    iin = Column(String(12), unique=True)
    position = Column(String(200))
    status = Column(String(100))

class Meeting(Base):
    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True)
    number = Column(String(50), unique=True)
    date = Column(String(20))
    status = Column(String(50), default="Проект")
    agenda_items = relationship("AgendaItem", back_populates="meeting", cascade="all, delete-orphan")

class AgendaItem(Base):
    __tablename__ = "agenda_items"
    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    number = Column(Integer)
    title = Column(String(500))
    description = Column(Text)
    meeting = relationship("Meeting", back_populates="agenda_items")
    votes = relationship("Vote", back_populates="agenda_item", cascade="all, delete-orphan")
    decision = relationship("Decision", uselist=False, back_populates="agenda_item", cascade="all, delete-orphan")

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    agenda_item_id = Column(Integer, ForeignKey("agenda_items.id"))
    director_id = Column(Integer, ForeignKey("directors.id"))
    choice = Column(String(20))
    ecp_signature = Column(String(500))
    timestamp = Column(DateTime, default=datetime.datetime.now)
    agenda_item = relationship("AgendaItem", back_populates="votes")

class Decision(Base):
    __tablename__ = "decisions"
    id = Column(Integer, primary_key=True)
    agenda_item_id = Column(Integer, ForeignKey("agenda_items.id"), unique=True)
    text = Column(Text)
    result = Column(String(100))
    agenda_item = relationship("AgendaItem", back_populates="decision")
''')

# app/schemas.py
open("app/schemas.py","w", encoding="utf-8").write('''
from pydantic import BaseModel
from typing import List

class DirectorCreate(BaseModel):
    fio: str
    birth_date: str
    iin: str
    position: str
    status: str

class AgendaItemCreate(BaseModel):
    number: int
    title: str
    description: str

class MeetingCreate(BaseModel):
    number: str
    date: str
    items: List[AgendaItemCreate]

class VoteCreate(BaseModel):
    agenda_item_id: int
    director_id: int
    choice: str
    ecp_signature: str
''')

# app/ecp.py
open("app/ecp.py","w", encoding="utf-8").write('''
import hashlib
def verify_ecp(iin: str, ecp_signature: str, data: str) -> bool:
    if not ecp_signature or len(ecp_signature) < 10:
        return False
    return "VALID" in ecp_signature or iin in ecp_signature

def create_ecp_mock(iin: str, data: str) -> str:
    h = hashlib.sha256((iin + data).encode()).hexdigest()
    return f"ECP_VALID_{iin}_{h[:20]}"
''')

# app/voting.py
open("app/voting.py","w", encoding="utf-8").write('''
from sqlalchemy.orm import Session
from. import models
from.ecp import verify_ecp

def vote(db: Session, agenda_item_id: int, director_id: int, choice: str, ecp: str):
    director = db.query(models.Director).get(director_id)
    if not director:
        return {"error": "Директор не найден"}
    if not verify_ecp(director.iin, ecp, f"{agenda_item_id}{choice}"):
        return {"error": "ЭЦП не верна!"}
    v = models.Vote(agenda_item_id=agenda_item_id, director_id=director_id, choice=choice, ecp_signature=ecp)
    db.add(v)
    db.commit()
    return {"status": f"{director.fio} проголосовал: {choice}"}

def get_results(db: Session, agenda_item_id: int):
    votes = db.query(models.Vote).filter_by(agenda_item_id=agenda_item_id).all()
    return {
        "ЗА": len([v for v in votes if v.choice == "ЗА"]),
        "ПРОТИВ": len([v for v in votes if v.choice == "ПРОТИВ"]),
        "ВОЗДЕРЖАЛСЯ": len([v for v in votes if v.choice == "ВОЗДЕРЖАЛСЯ"]),
        "ВСЕГО": len(votes),
        "детали": [{"fio": db.query(models.Director).get(v.director_id).fio, "choice": v.choice} for v in votes]
    }
''')

# app/agenda.py
open("app/agenda.py","w", encoding="utf-8").write('''
from sqlalchemy.orm import Session
from. import models, schemas

def create_meeting_with_agenda(db: Session, data: schemas.MeetingCreate):
    meeting = models.Meeting(number=data.number, date=data.date, status="Проект")
    db.add(meeting)
    db.flush()
    for item_data in data.items:
        item = models.AgendaItem(meeting_id=meeting.id, number=item_data.number, title=item_data.title, description=item_data.description)
        db.add(item)
    db.commit()
    db.refresh(meeting)
    return meeting
''')

# app/protocol.py
open("app/protocol.py","w", encoding="utf-8").write('''
from sqlalchemy.orm import Session
from. import models
from.voting import get_results

def generate_protocol(db: Session, meeting_id: int):
    meeting = db.query(models.Meeting).get(meeting_id)
    if not meeting:
        return "Заседание не найдено"
    text = f"ПРОТОКОЛ №{meeting.number} от {meeting.date}\\nСтатус: {meeting.status}\\n\\n"
    for item in sorted(meeting.agenda_items, key=lambda x: x.number):
        res = get_results(db, item.id)
        text += f"ВОПРОС №{item.number}: {item.title}\\nОписание: {item.description}\\n"
        text += f"ГОЛОСОВАНИЕ: ЗА={res['ЗА']}, ПРОТИВ={res['ПРОТИВ']}, ВОЗДЕРЖАЛСЯ={res['ВОЗДЕРЖАЛСЯ']}\\n"
        text += "---\\n\\n"
    return text
''')

# app/main.py
open("app/main.py","w", encoding="utf-8").write('''
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from.database import Base, engine, get_db
from. import models, schemas
from.agenda import create_meeting_with_agenda
from.voting import vote, get_results
from.protocol import generate_protocol

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Совет Директоров - ЭЦП")

@app.post("/directors/")
def add_director(d: schemas.DirectorCreate, db: Session = Depends(get_db)):
    obj = models.Director(**d.dict())
    db.add(obj); db.commit(); db.refresh(obj)
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
''')

print("✅ Проект создан! Структура:")
print("sovet_directorov/")
print("├── requirements.txt")
print("└── app/ (8 файлов)")
print("\\nЗапуск: pip install -r requirements.txt && uvicorn app.main:app --reload")