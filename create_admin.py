import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# ВСТАВЬ СЮДА ТВОЙ DATABASE_URL ИЗ RENDER
DATABASE_URL = "postgresql://sovet_db_user:SxYPBAbq6xRgM2CAy4DFdOUOzElKMkRO@dpg-datu29navr4c73ev77m0-a/sovet_db"

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from app.routers import User  # или from app import models

db = SessionLocal()
existing = db.query(User).filter(User.username == "ADMIN").first()
if existing:
    print("Юзер уже есть, обновляю пароль...")
    existing.hashed_password = pwd_context.hash("Assa123$")
    db.commit()
    print("Пароль обновлен!")
else:
    user = User(
        username="ADMIN",
        hashed_password=pwd_context.hash("Assa123$"),
        role="admin",
        is_active=True
    )
    db.add(user)
    db.commit()
    print("Юзер ADMIN создан!")

db.close()