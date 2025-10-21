import typing
import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import  Mapped, mapped_column,relationship
from sqlalchemy.sql import func

if typing.TYPE_CHECKING:
    from src.models.UserModel import User


from src.db import Base

class Note(Base):
    __tablename__ = "note"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    username: Mapped["User"] = relationship(back_populates="notes", uselist=False)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=True)
    tags: Mapped[list["Tags"]] = relationship(secondary="notetags", back_populates="notes", uselist=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now())

class Tags(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    notes: Mapped[list["Note"]] = relationship(secondary="notetags", back_populates="tags", uselist=True)

class NoteTags(Base):
    __tablename__ = "notetags"

    note_id: Mapped[int] = mapped_column(ForeignKey("note.id"), primary_key=True)
    tagse_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)