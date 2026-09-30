from fastapi import APIRouter

router = APIRouter(prefix="/directors", tags=["directors"])

@router.get("/")
def get_directors():
    return [{"id": 1, "name": "Test Director"}]

@router.post("/")
def create_director(name: str):
    return {"id": 2, "name": name}
