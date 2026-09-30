from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
import os

db_url = os.getenv("DATABASE_URL", "")
if db_url.startswith("postgres://"):
    os.environ["DATABASE_URL"] = db_url.replace("postgres://", "postgresql://", 1)

Base.metadata.create_all(bind=engine)

from app.routers import directors, auth, meetings, users

app = FastAPI(title="Совет Директоров v2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(directors.router)
app.include_router(meetings.router, prefix="/meetings", tags=["Meetings"])

@app.get("/")
def root():
    return {"status": "ok", "version": "v2"}