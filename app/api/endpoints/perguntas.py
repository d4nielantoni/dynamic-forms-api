from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.crud import pergunta as crud_pergunta
from app.schemas.pergunta import Pergunta, PerguntaCreate, PerguntaUpdate

router = APIRouter()

@router.get("/", response_model=List[Pergunta])
def read_perguntas(
    skip: int = 0, 
    limit: int = 100,
    formulario_id: Optional[int] = None,
    tipo_pergunta: Optional[str] = None,
    obrigatoria: Optional[bool] = None,
    sub_pergunta: Optional[bool] = None,
    sort_by: str = "ordem",
    sort_order: str = "asc",
    db: Session = Depends(get_db)
):
    """
    Recupera uma lista de perguntas com suporte a:
    - Filtros (por tipo, obrigatoriedade, etc.)
    - Ordenação
    - Paginação
    """
    perguntas = crud_pergunta.get_perguntas(
        db, 
        skip=skip, 
        limit=limit,
        formulario_id=formulario_id,
        tipo_pergunta=tipo_pergunta,
        obrigatoria=obrigatoria,
        sub_pergunta=sub_pergunta,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return perguntas

@router.post("/", response_model=Pergunta, status_code=status.HTTP_201_CREATED)
def create_pergunta(
    pergunta: PerguntaCreate, 
    db: Session = Depends(get_db)
):
    """
    Cria uma nova pergunta.
    """
    return crud_pergunta.create_pergunta(db=db, pergunta=pergunta)

@router.get("/{pergunta_id}", response_model=Pergunta)
def read_pergunta(
    pergunta_id: int, 
    db: Session = Depends(get_db)
):
    """
    Recupera uma pergunta específica pelo ID.
    """
    db_pergunta = crud_pergunta.get_pergunta(db, pergunta_id=pergunta_id)
    if db_pergunta is None:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    return db_pergunta

@router.put("/{pergunta_id}", response_model=Pergunta)
def update_pergunta(
    pergunta_id: int, 
    pergunta: PerguntaUpdate, 
    db: Session = Depends(get_db)
):
    """
    Atualiza uma pergunta existente.
    """
    db_pergunta = crud_pergunta.update_pergunta(db, pergunta_id=pergunta_id, pergunta=pergunta)
    if db_pergunta is None:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    return db_pergunta

@router.delete("/{pergunta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pergunta(
    pergunta_id: int, 
    db: Session = Depends(get_db)
):
    """
    Remove uma pergunta.
    """
    success = crud_pergunta.delete_pergunta(db, pergunta_id=pergunta_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    return None

@router.get("/formulario/{formulario_id}", response_model=List[Pergunta])
def read_perguntas_by_formulario(
    formulario_id: int,
    skip: int = 0, 
    limit: int = 100,
    tipo_pergunta: Optional[str] = None,
    obrigatoria: Optional[bool] = None,
    sub_pergunta: Optional[bool] = None,
    sort_by: str = "ordem",
    sort_order: str = "asc",
    db: Session = Depends(get_db)
):
    """
    Recupera todas as perguntas de um formulário específico com suporte a:
    - Filtros (por tipo, obrigatoriedade, etc.)
    - Ordenação
    - Paginação
    """
    perguntas = crud_pergunta.get_perguntas(
        db, 
        skip=skip, 
        limit=limit,
        formulario_id=formulario_id,
        tipo_pergunta=tipo_pergunta,
        obrigatoria=obrigatoria,
        sub_pergunta=sub_pergunta,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return perguntas
