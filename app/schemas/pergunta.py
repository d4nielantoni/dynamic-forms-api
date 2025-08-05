from typing import Optional, List
from pydantic import BaseModel

# Schemas para OpcoesRespostas
class OpcoesRespostasBase(BaseModel):
    resposta: Optional[str] = None
    ordem: Optional[int] = 0
    resposta_aberta: Optional[bool] = False

class OpcoesRespostasCreate(OpcoesRespostasBase):
    id_pergunta: int

class OpcoesRespostasUpdate(OpcoesRespostasBase):
    pass

class OpcoesRespostasInDB(OpcoesRespostasBase):
    id: int
    id_pergunta: int

    class Config:
        orm_mode = True

class OpcoesRespostas(OpcoesRespostasInDB):
    pass

# Schemas para OpcaoResposta
class OpcaoRespostaBase(BaseModel):
    id_opcao_resposta: int
    id_pergunta: int

class OpcaoRespostaCreate(OpcaoRespostaBase):
    pass

class OpcaoRespostaUpdate(OpcaoRespostaBase):
    pass

class OpcaoRespostaInDB(OpcaoRespostaBase):
    id: int

    class Config:
        orm_mode = True

class OpcaoResposta(OpcaoRespostaInDB):
    pass

# Schemas para Pergunta
class PerguntaBase(BaseModel):
    id_formulario: int
    titulo: str
    codigo: Optional[str] = None
    orientacao_resposta: Optional[str] = None
    ordem: Optional[int] = 0
    obrigatoria: Optional[bool] = False
    sub_pergunta: Optional[bool] = False
    tipo_pergunta: str

class PerguntaCreate(PerguntaBase):
    opcoes_respostas_multiplas: Optional[List[OpcoesRespostasBase]] = []

class PerguntaUpdate(PerguntaBase):
    id_formulario: Optional[int] = None
    titulo: Optional[str] = None
    tipo_pergunta: Optional[str] = None

class PerguntaInDB(PerguntaBase):
    id: int

    class Config:
        orm_mode = True

class Pergunta(PerguntaInDB):
    opcoes_respostas: List[OpcaoResposta] = []
    opcoes_respostas_multiplas: List[OpcoesRespostas] = []
