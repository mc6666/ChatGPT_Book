from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    line_id: Mapped[str] = mapped_column(String(30), unique=True)
    display_name: Mapped[str] = mapped_column(String(30))
    topic: Mapped[str] = mapped_column(String(20))

class Model(Base):
    __tablename__ = "models"
    id: Mapped[int] = mapped_column(primary_key=True)
    topic: Mapped[str] = mapped_column(String(20), unique=True)
    model_id: Mapped[str] = mapped_column(String(30))
    api_function: Mapped[str] = mapped_column(String(30))
    system_prompt: Mapped[str] = mapped_column(String(50))
    temperature: Mapped[float]
    max_tokens: Mapped[int]

