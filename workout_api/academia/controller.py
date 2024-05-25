from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.academia.schemas import AcademiaIn, AcademiaOut
from workout_api.academia.models import AcademiaModel

router = APIRouter()

@router.post(
    '/', 
    summary='Criar nova academia',
    status_code=status.HTTP_201_CREATED,
    response_model= AcademiaOut,
)
async def post(
    db_session: DatabaseDependency, 
    academia_in: AcademiaIn = Body(...)
)-> AcademiaOut:    
    try: 
        academia_out = AcademiaOut(id=uuid4(), **academia_in.model_dump())
        academia_model = AcademiaModel(**academia_out.model_dump())
        
        db_session.add(academia_model)
        await db_session.commit()

    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe uma academia cadastrada com o nome: {academia_in.cpf}'
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='Ocorreu um erro ao inserir os dados no banco'
        )

    return academia_out

@router.get(
    '/', 
    summary='Consultar todos as academias',
    status_code=status.HTTP_200_OK,
    response_model= list[AcademiaOut],
)
async def query(
    db_session: DatabaseDependency, 
)-> list[AcademiaOut]:
    academias: list[AcademiaOut] = (await db_session.execute(select(AcademiaModel))).scalars().all()
    return academias

@router.get(
    '/{id}', 
    summary='Consultar uma academia',
    status_code=status.HTTP_200_OK,
    response_model= AcademiaOut,
)
async def query(
    id: UUID4,db_session: DatabaseDependency, 
)-> AcademiaOut:
    academia: AcademiaOut = (
        await db_session.execute(select(AcademiaModel).filter_by(id=id))
    ).scalars().first()

    if not academia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Academia não encontrada com id: {id} '
        )

    return academia