from app.characters import schemas
from app.characters.models import Character
from app.dao.base import BaseDAO
from fastapi import HTTPException, status

from app.users import models


class CharactersDAO(BaseDAO):
    model = Character


