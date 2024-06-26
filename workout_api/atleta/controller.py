from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import LimitOffsetPage, add_pagination, paginate
from sqlalchemy.exc import IntegrityError
from pydantic import UUID4
from sqlalchemy.future import select
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.atleta.schemas import AtletaGetAll, AtletaIn, AtletaOut, AtletaUpdate
from workout_api.atleta.models import AtletaModel
from workout_api.treinos.models import TreinoModel
from workout_api.academia.models import AcademiaModel
    
router = APIRouter()

@router.post(
    '/', 
    summary='Criar novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(
    db_session: DatabaseDependency, 
    atleta_in: AtletaIn = Body(...)
):  
    treino_nome = atleta_in.treino.nome
    academia_nome = atleta_in.academia.nome

    treino = (await db_session.execute(
        select(TreinoModel).filter_by(nome=treino_nome))
    ).scalars().first() 

    if not treino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Treino {treino_nome} não encontrado'
        )
    

    academia = (await db_session.execute(
        select(AcademiaModel).filter_by(nome=academia_nome))
    ).scalars().first() 

    if not academia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Academia {academia_nome} não encontrado'
        )
    try: 
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'treino', 'academia'}))

        atleta_model.treino_id = treino.pk_id
        atleta_model.academia_id = academia.pk_id
        
        db_session.add(atleta_model)
        await db_session.commit()

    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f'Já existe um atleta cadastrado com o cpf: {atleta_out.cpf}'
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='Ocorreu um erro ao inserir os dados no banco'
        )

    return atleta_out


@router.get(
    '/',  
    summary='Consultar todos os Atletas',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[AtletaGetAll],
)
async def query(db_session: DatabaseDependency, nome: str | None = None, cpf: str | None = None) -> list[AtletaOut]:
    atletas: list[AtletaGetAll] = (await db_session.execute(select(AtletaModel))).scalars().all()
    if nome:
        atletas = [atleta for atleta in atletas if atleta.nome == nome]
    if cpf:
        atletas = [atleta for atleta in atletas if atleta.cpf == cpf]

    return paginate(atletas)

add_pagination(router)

@router.get(
    '/{id}', 
    summary='Consultar um atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model= AtletaOut,
)
async def query(
    id: UUID4,db_session: DatabaseDependency, 
)-> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado com id: {id} '
        )

    return atleta

@router.patch(
    '/{id}', 
    summary='Editar um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model= AtletaOut,
)
async def patch(
    id: UUID4,db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...) 
)-> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado com id: {id} '
        )
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)
    
    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta

@router.delete(
    '/{id}', 
    summary='Deletar um atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def query(
    id: UUID4,db_session: DatabaseDependency, 
)-> None:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Treino não encontrado com id: {id} '
        )

    await db_session.delete(atleta)
    await db_session.commit()
