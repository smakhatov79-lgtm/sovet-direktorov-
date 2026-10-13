
from pydantic import BaseModel, Field
from typing import List
from typing import Literal
from datetime import date

class DirectorCreate(BaseModel):
    last_name: str = Field(..., description="Фамилия")
    first_name: str = Field(..., description="Имя")
    middle_name: str = Field(..., description="Отчество")
    iin: str = Field(..., pattern=r"^\d{12}$", description="ИИН должен состоять ровно из 12 цифр")
    birth_date: date = Field(..., description="Дата рождения - из календаря")
    position: str = Field(..., description="Должность")
    status: Literal[
        "Председатель Совета директоров",
        "член Совета директоров",
        "член Совета директоров-независимый директор",
        "приглашенное лицо"
    ]

class DirectorOut(BaseModel):
    id: int
    last_name: str
    first_name: str
    middle_name: str
    iin: str
    birth_date: date
    position: str
    status: str
    fio: str = "" # для совместимости

    class Config:
        from_attributes = True