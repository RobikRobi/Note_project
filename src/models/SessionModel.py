from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
import uuid
from src.db import Base


class SessionUser(Base):
    __tablename__ = "ses_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_id"))
    key: Mapped[uuid.UUID] = mapped_column(unique=True)
