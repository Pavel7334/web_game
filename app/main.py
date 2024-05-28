from fastapi import FastAPI

from app.users.router import router as users_router
from app.characters.router import router as characters_router

app = FastAPI()

app.include_router(users_router)
app.include_router(characters_router)
