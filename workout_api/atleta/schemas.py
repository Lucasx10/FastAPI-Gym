from typing import Annotated, Optional
from pydantic import Field, PositiveFloat

from workout_api.contrib.schemas import BaseSchema, OutMixin
from workout_api.treinos.schemas import TreinoIn
from workout_api.academia.schemas import AcademiaAtleta

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta')]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=69.9)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.70)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]
    treino: Annotated[TreinoIn, Field(description='Treino do atleta')]
    academia: Annotated[AcademiaAtleta, Field(description='Academia do atleta')]

class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta')]
    peso: Annotated[Optional[PositiveFloat], Field(None, description='Peso do atleta', example=69.9)]