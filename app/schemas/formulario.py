from typing import Optional, List
from pydantic import BaseModel

# Schemas para Formulario
class FormularioBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    ordem: Optional[int] = 0

class FormularioCreate(FormularioBase):
    pass

class FormularioUpdate(FormularioBase):
    titulo: Optional[str] = None

class FormularioInDB(FormularioBase):
    id: int

    class Config:
        orm_mode = True

class Formulario(FormularioInDB):
    pass
