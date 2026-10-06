from fastapi import APIRouter

router = APIRouter(prefix="/meetings", tags=["meetings"])

@router.get("/")
def get_meetings():
    return []

@router.post("/")
def create_meeting(title: str):
    return {"id": 1, "title": title}