from fastapi import APIRouter
from workout_api.atleta.controller import router as atleta
from workout_api.treinos.controller import router as treino
from workout_api.academia.controller import router as academia

api_router = APIRouter()
api_router.include_router(atleta, prefix='/atletas', tags=['atletas'])
api_router.include_router(treino, prefix='/treinos', tags=['treinos'])
api_router.include_router(academia, prefix='/academias', tags=['academias'])
