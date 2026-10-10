import os
# 1. Сначала фиксим URL
db_url = os.getenv("DATABASE_URL", "")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
    os.environ["DATABASE_URL"] = db_url

# 2. Только потом импорты
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import directors, auth, meetings, users

# 3. Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ASSA Corporate Portal v2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # для v2 пока так
    allow_credentials=False, # ВАЖНО: False когда "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(directors.router)
app.include_router(meetings.router, prefix="/meetings", tags=["Meetings"])

@app.get("/")
def root():
    return {"status": "ok", "version": "v2"}