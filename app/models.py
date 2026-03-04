from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import TIMESTAMP, text
from datetime import datetime
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[bool] = mapped_column(server_default='True', nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE" ), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__= "users"
    email: Mapped[str] = mapped_column(String, nullable=False, unique= True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__="votes"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE" ), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE" ), primary_key=True)