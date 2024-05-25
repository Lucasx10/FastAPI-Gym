from typing import Annotated
from pydantic import UUID4, Field, PositiveFloat

from workout_api.contrib.schemas import BaseSchema

class AcademiaIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da academia', example='Trinity', max_length=50)]
    endereco: Annotated[str, Field(description='Endereco da academia', example='Av. das flores, 100', max_length=80)]
    proprietario: Annotated[str, Field(description='Proprietario da academia', example='João', max_length=30)]

class AcademiaAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome da academia', example='Trinity', max_length=50)]

class AcademiaOut(AcademiaIn):
    id: Annotated[UUID4, Field(description="Identificador da academia")]