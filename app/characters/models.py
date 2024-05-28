from datetime import datetime
from typing import Union

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import relationship

from app.database import Base


class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True, doc="Уникальный идентификатор персонажа")
    name = Column(String, nullable=False, doc="Имя персонажа")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, doc="ID пользователя, владеющего персонажем")
    level = Column(Integer, default=1, doc="Уровень персонажа")
    experience = Column(Float, default=0.0, doc="Опыт персонажа")
    strength = Column('strength', Integer, default=1, doc="Сила персонажа")
    agility = Column('agility', Integer, default=1, doc="Ловкость персонажа")
    intellect = Column('intellect', Integer, default=1, doc="Интеллект персонажа")
    class_ = Column(Enum("Warrior", "Mage", "Archer", name="class_enum"), doc="Класс персонажа")
    race = Column(Enum("Human", "Elf", "Dwarf", "Orc", name="race_enum"), doc="Раса персонажа")
    health = Column(Float, default=100.0, doc="Здоровье персонажа")
    mana = Column(Float, default=100.0, doc="Мана персонажа")
    abilities = Column(Enum("Fireball", "Heal", "Stealth", "Double Strike", name="abilities_enum"),
                        doc="Способности персонажа")
    history = Column(String, doc="История персонажа")
    faction = Column(Enum("Alliance", "Horde", name="faction_enum"), doc="Фракция персонажа")
    creation_date = Column(DateTime, default=datetime.utcnow, doc="Дата создания персонажа")
    last_updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                               doc="Дата последнего обновления информации о персонаже")

    users = relationship(
        "User",
        secondary="user_characters",
        back_populates="characters",
        doc="Пользователи, владеющие персонажем")


class UserCharacter(Base):
    __tablename__ = 'user_characters'

    id = Column(
        Integer, primary_key=True, index=True,
        doc="Уникальный идентификатор связи между пользователем и персонажем"
    )
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, doc="ID пользователя, владеющего персонажем")
    character_id = Column(Integer, ForeignKey('characters.id'), nullable=False, doc="ID персонажа")
