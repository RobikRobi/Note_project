import datetime
import typing

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import  Mapped, mapped_column,relationship
from sqlalchemy.sql import func

from src.db import Base

class Message(Base):
    __tablename__ = "note_table"

    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(nullable=True)
    content:Mapped[str] = mapped_column(nullable=True)
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    text:Mapped[str]