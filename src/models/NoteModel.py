import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import  Mapped, mapped_column,relationship
from sqlalchemy.sql import func


from src.db import Base

class Note(Base):
    __tablename__ = "note_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_table.id'))
    title: Mapped[list["Tags"]] = relationship(secondary="notetags_table", back_populates="notes", uselist=True)
    content: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now())

class Tags(Base):
    __tablename__ = "tags_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    notes: Mapped[list["Note"]] = relationship(secondary="notetags_table", back_populates="title", uselist=True)

class NoteTags(Base):
    __tablename__ = "notetags_table"

    note_id: Mapped[int] = mapped_column(ForeignKey('note_table.id'), primary_key=True)
    tagse_id: Mapped[int] = mapped_column(ForeignKey('tags_table.id'), primary_key=True)