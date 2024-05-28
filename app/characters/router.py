from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.characters.dao import CharactersDAO
from app.characters.models import Character
from app.characters.schemas import SCharacterCreate, CharacterCreate
from app.database import async_session_maker
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter()


@router.get("/characters/", response_model=List[CharacterCreate])
async def get_user_characters(user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    async with async_session_maker() as session:
        stmt = select(Character).where(Character.user_id == user.id)
        result = await session.execute(stmt)
        characters = result.scalars().all()

    return characters


@router.post("/characters", status_code=status.HTTP_201_CREATED, response_model=CharacterCreate)
async def create_character(character: SCharacterCreate, current_user: User = Depends(get_current_user)):
    valid_abilities = {
        "Mage": ["Fireball", "Heal"],
        "Warrior": ["Double Strike"],
        "Archer": ["Stealth"]
    }

    # Проверяем, что класс персонажа и его способности соответствуют допустимым значениям
    if character.class_ not in valid_abilities:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Недопустимый класс персонажа: {character.class_}")

    if any(ability not in valid_abilities[character.class_] for ability in character.abilities):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Недопустимые способности для класса {character.class_}")

    # Создаем словарь с данными для создания персонажа
    character_data = character.dict()
    character_data['user_id'] = current_user.id

    # Если у персонажа есть способности, преобразуем их в строку и добавляем в данные персонажа
    if character.abilities:
        character_data['abilities'] = ','.join(character.abilities)

    new_character = await CharactersDAO.create(character_data)
    return new_character


@router.delete("/characters/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_character(character_id: int, user: User = Depends(get_current_user)):
    await CharactersDAO.delete(character_id, user.id)
    return None
