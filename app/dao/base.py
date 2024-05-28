from sqlalchemy import select, insert

from app.database import async_session_maker
from fastapi import HTTPException, status


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def create(cls, data):
        async with async_session_maker() as session:
            instance = cls.model(**data)
            session.add(instance)
            await session.commit()
            return instance

    @classmethod
    async def delete(cls, model_id: int, user_id: int):
        async with async_session_maker() as session:
            instance = await session.get(cls.model, model_id)
            if instance is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Персонажа с id {model_id} не найден")

            if instance.user_id != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="У вас нет прав для удаления этого объекта")

            await session.delete(instance)
            await session.commit()