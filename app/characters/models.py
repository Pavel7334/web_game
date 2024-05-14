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
    _strength = Column('strength', Integer, default=1, doc="Сила персонажа")
    _agility = Column('agility', Integer, default=1, doc="Ловкость персонажа")
    _intellect = Column('intellect', Integer, default=1, doc="Интеллект персонажа")
    class_ = Column(Enum("Warrior", "Mage", "Archer", name="class_enum"), doc="Класс персонажа")
    race = Column(Enum("Human", "Elf", "Dwarf", "Orc", name="race_enum"), doc="Раса персонажа")
    health = Column(Float, default=100.0, doc="Здоровье персонажа")
    _mana = Column(Float, default=100.0, doc="Мана персонажа")
    _abilities = Column(Enum("Fireball", "Heal", "Stealth", "Double Strike", name="abilities_enum"),
                        doc="Способности персонажа")
    history = Column(String, doc="История персонажа")
    faction = Column(Enum("Alliance", "Horde", name="faction_enum"), doc="Фракция персонажа")
    creation_date = Column(DateTime, default=datetime.utcnow, doc="Дата создания персонажа")
    last_updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                               doc="Дата последнего обновления информации о персонаже")

    users = relationship(
        "User",
        secondary="user_character",
        back_populates="characters",
        doc="Пользователи, владеющие персонажем")

    @property
    def strength(self) -> int:
        """
        Возвращает значение силы персонажа.
        """
        return self._strength

    @strength.setter
    def strength(self, value: int) -> None:
        """
        Устанавливает значение силы персонажа.

        Параметры:
        - value: int, значение силы персонажа.
        """
        if 0 < value <= 10 and self._agility + self._intellect + value <= 10:
            self._strength = value

    @property
    def agility(self) -> int:
        """
        Возвращает значение ловкости персонажа.
        """
        return self._agility

    @agility.setter
    def agility(self, value: int) -> None:
        """
        Устанавливает значение ловкости персонажа.

        Параметры:
        - value: int, значение ловкости персонажа.
        """
        if 0 < value <= 10 and self._strength + self._intellect + value <= 10:
            self._agility = value

    @property
    def intellect(self) -> int:
        """
        Возвращает значение интеллекта персонажа.
        """
        return self._intellect

    @intellect.setter
    def intellect(self, value: int) -> None:
        """
        Устанавливает значение интеллекта персонажа.

        Параметры:
        - value: int, значение интеллекта персонажа.
        """
        if 0 < value <= 10 and self._strength + self._agility + value <= 10:
            self._intellect = value

    @property
    def abilities(self) -> Union[str, None]:
        """
        Возвращает способности персонажа.
        """
        return self._abilities

    @abilities.setter
    def abilities(self, value: str) -> None:
        """
        Устанавливает способности персонажа в зависимости от его класса.

        Параметры:
        - value: str, способность персонажа.

        Исключения:
        - ValueError: выбрасывается, если класс персонажа не поддерживает указанную способность.
        """
        if self.class_ == "Mage" and value in ("Fireball", "Heal"):
            self._abilities = value
        elif self.class_ == "Warrior" and value == "Double Strike":
            self._abilities = value
        elif self.class_ == "Archer" and value == "Stealth":
            self._abilities = value
        else:
            raise ValueError(f"Класс '{self.class_}' не может иметь способность '{value}'.")

    @property
    def mana(self) -> Union[float, None]:
        """
        Возвращает значение маны персонажа.
        """
        return self._mana

    @mana.setter
    def mana(self, value: float) -> None:
        """
        Устанавливает значение маны персонажа, если класс персонажа - Mage.

        Параметры:
        - value: float, значение маны персонажа.

        Исключения:
        - ValueError: выбрасывается, если класс персонажа не является Mage.
        """
        if self.class_ == "Mage":
            self._mana = value
        else:
            raise ValueError("Поле 'mana' может быть установлено только для персонажей класса 'Mage'.")


class UserCharacter(Base):
    __tablename__ = 'user_characters'

    id = Column(
        Integer, primary_key=True, index=True,
        doc="Уникальный идентификатор связи между пользователем и персонажем"
    )
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, doc="ID пользователя, владеющего персонажем")
    character_id = Column(Integer, ForeignKey('characters.id'), nullable=False, doc="ID персонажа")
