
from sqlalchemy.orm import Session
from. import models
from.voting import get_results

def generate_protocol(db: Session, meeting_id: int):
    meeting = db.query(models.Meeting).get(meeting_id)
    if not meeting:
        return "Заседание не найдено"
    text = f"ПРОТОКОЛ №{meeting.number} от {meeting.date}\nСтатус: {meeting.status}\n\n"
    for item in sorted(meeting.agenda_items, key=lambda x: x.number):
        res = get_results(db, item.id)
        text += f"ВОПРОС №{item.number}: {item.title}\nОписание: {item.description}\n"
        text += f"ГОЛОСОВАНИЕ: ЗА={res['ЗА']}, ПРОТИВ={res['ПРОТИВ']}, ВОЗДЕРЖАЛСЯ={res['ВОЗДЕРЖАЛСЯ']}\n"
        text += "---\n\n"
    return text
