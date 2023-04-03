from fastapi import APIRouter

from app.api import login, users

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.path, prefix="/users", tags=["users"])