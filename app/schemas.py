
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
