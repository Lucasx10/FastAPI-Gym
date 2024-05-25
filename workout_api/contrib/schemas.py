from datetime import datetime
from typing import Annotated
from pydantic import UUID4, BaseModel, Field

class BaseSchema(BaseModel):
    class config:
        extra = 'forbid'
        from_atributes = True

class OutMixin(BaseModel):
    id: Annotated[UUID4, Field(description="Identificador")]
    created_at: Annotated[datetime, Field(description="Data de criação")]