import datetime
import typing

from sqlalchemy import DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey

if typing.TYPE_CHECKING:
    from src.models.MarkModel import Mark
    from src.models.GroupModel import Group
    from src.models.LessonModel import Lesson

from src.db import Base


class User(Base):
    __tablename__ = "user_table"

    id:Mapped[int] = mapped_column(primary_key=True)

    login:Mapped[str] = mapped_column(unique=True)
    password:Mapped[bytes]
    name:Mapped[str]