
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
