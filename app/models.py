
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
