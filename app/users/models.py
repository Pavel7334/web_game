from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, doc="Уникальный идентификатор пользователя")
    email = Column(String, unique=True, nullable=False, doc="Email пользователя")
    username = Column(String, unique=True, index=True, nullable=False, doc="Имя пользователя")
    password = Column(String, nullable=False, doc="Хэшированный пароль пользователя")

    characters = relationship(
        "Character",
        secondary="user_characters",
        back_populates="users",
        doc="Персонажи, принадлежащие пользователю")