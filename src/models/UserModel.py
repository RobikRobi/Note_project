import typing
from sqlalchemy.orm import Mapped, mapped_column, relationship


from src.db import Base

if typing.TYPE_CHECKING:
    from src.models.NoteModel import Note

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)

    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    name: Mapped[str]
    notes: Mapped[list["Note"]] = relationship(back_populates="username", uselist=True)