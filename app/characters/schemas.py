from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class CharacterClass(str, Enum):
    Mage = "Mage"
    Warrior = "Warrior"
    Archer = "Archer"


class Race(str, Enum):
    Human = "Human"
    Elf = "Elf"
    Dwarf = "Dwarf"
    Orc = "Orc"


class Faction(str, Enum):
    Alliance = "Alliance"
    Horde = "Horde"


class Ability(str, Enum):
    Fireball = "Fireball"
    Heal = "Heal"
    Stealth = "Stealth"
    Double_Strike = "Double Strike"


class SCharacterCreate(BaseModel):
    name: str = Field(..., description="Имя персонажа", min_length=1, max_length=50)
    level: Optional[int] = Field(1, description="Уровень персонажа")
    experience: Optional[float] = Field(0.0, description="Опыт персонажа")
    strength: Optional[int] = Field(1, description="Сила персонажа")
    agility: Optional[int] = Field(1, description="Ловкость персонажа")
    intellect: Optional[int] = Field(1, description="Интеллект персонажа")
    class_: CharacterClass = Field(..., description="Класс персонажа")
    race: Race = Field(..., description="Раса персонажа")
    health: Optional[float] = Field(100.0, description="Здоровье персонажа")
    mana: Optional[float] = Field(100.0, description="Мана персонажа (только для Мага)")
    abilities: Optional[List[Ability]] = Field(None, description="Способности персонажа")
    history: Optional[str] = Field(None, description="История персонажа")
    faction: Optional[Faction] = Field(None, description="Фракция персонажа")


class Character(BaseModel):
    id: int
    name: str
    user_id: int
    level: int
    experience: float
    strength: int
    agility: int
    intellect: int
    class_: CharacterClass
    race: Race
    health: float
    mana: float
    abilities: List[Ability]
    history: Optional[str]
    faction: Optional[Faction]

    class Config:
        from_attributes = True


class CharacterCreate(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
