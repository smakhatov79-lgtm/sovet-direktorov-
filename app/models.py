from sqlalchemy import Column, Integer, String, Boolean, Date
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    role = Column(String(20), default="admin") # admin, secretary, director, viewer
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
class Director(Base):
    __tablename__ = "directors"
    
    id = Column(Integer, primary_key=True)
    last_name = Column(String) # Фамилия
    first_name = Column(String) # Имя
    middle_name = Column(String) # Отчество
    iin = Column(String, unique=True) # ИИН 12 цифр
    birth_date = Column(Date)
    position = Column(String) # Должность, сами заполняем
    status = Column(String) # Статус из списка