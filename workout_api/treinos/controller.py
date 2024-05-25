from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.treinos.schemas import TreinoIn, TreinoOut
from workout_api.treinos.models import TreinoModel

router = APIRouter()

@router.post(
    '/', 
    summary='Criar novo treino',
    status_code=status.HTTP_201_CREATED,
    response_model= TreinoOut,
)
async def post(
    db_session: DatabaseDependency, 
    treino_in: TreinoIn = Body(...)
)-> TreinoOut: 
    
    treino_out = TreinoOut(id=uuid4(), **treino_in.model_dump())
    treino_model = TreinoModel(**treino_out.model_dump())
    
    db_session.add(treino_model)
    await db_session.commit()

    return treino_out

@router.get(
    '/', 
    summary='Consultar todos os treinos',
    status_code=status.HTTP_200_OK,
    response_model= list[TreinoOut],
)
async def query(
    db_session: DatabaseDependency, 
)-> list[TreinoOut]:
    treinos: list[TreinoOut] = (await db_session.execute(select(TreinoModel))).scalars().all()
    return treinos

@router.get(
    '/{id}', 
    summary='Consultar um treino',
    status_code=status.HTTP_200_OK,
    response_model= TreinoOut,
)
async def query(
    id: UUID4,db_session: DatabaseDependency, 
)-> TreinoOut:
    treino: TreinoOut = (
        await db_session.execute(select(TreinoModel).filter_by(id=id))
    ).scalars().first()

    if not treino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Treino não encontrado com id: {id} '
        )

    return treino