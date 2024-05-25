from typing import Annotated
from pydantic import UUID4, Field, PositiveFloat

from workout_api.contrib.schemas import BaseSchema

class TreinoIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome do treino', example='Perna', max_length=50)]

class TreinoOut(TreinoIn):
    id: Annotated[UUID4, Field(description="Identificador da categoria")]