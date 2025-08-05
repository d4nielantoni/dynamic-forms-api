from fastapi import APIRouter

from app.api.endpoints import formularios, perguntas

api_router = APIRouter()
api_router.include_router(formularios.router, prefix="/formularios", tags=["formularios"])
api_router.include_router(perguntas.router, prefix="/perguntas", tags=["perguntas"])
