
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
