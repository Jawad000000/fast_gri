from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[bool] = mapped_column(server_default='True', nullable=False)