from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.crud import formulario as crud_formulario
from app.schemas.formulario import Formulario, FormularioCreate, FormularioUpdate

router = APIRouter()

@router.get("/", response_model=List[Formulario])
def read_formularios(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Recupera uma lista de formulários com paginação.
    """
    formularios = crud_formulario.get_formularios(db, skip=skip, limit=limit)
    return formularios

@router.post("/", response_model=Formulario, status_code=status.HTTP_201_CREATED)
def create_formulario(
    formulario: FormularioCreate, 
    db: Session = Depends(get_db)
):
    """
    Cria um novo formulário.
    """
    return crud_formulario.create_formulario(db=db, formulario=formulario)

@router.get("/{formulario_id}", response_model=Formulario)
def read_formulario(
    formulario_id: int, 
    db: Session = Depends(get_db)
):
    """
    Recupera um formulário específico pelo ID.
    """
    db_formulario = crud_formulario.get_formulario(db, formulario_id=formulario_id)
    if db_formulario is None:
        raise HTTPException(status_code=404, detail="Formulário não encontrado")
    return db_formulario

@router.put("/{formulario_id}", response_model=Formulario)
def update_formulario(
    formulario_id: int, 
    formulario: FormularioUpdate, 
    db: Session = Depends(get_db)
):
    """
    Atualiza um formulário existente.
    """
    db_formulario = crud_formulario.update_formulario(db, formulario_id=formulario_id, formulario=formulario)
    if db_formulario is None:
        raise HTTPException(status_code=404, detail="Formulário não encontrado")
    return db_formulario

@router.delete("/{formulario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_formulario(
    formulario_id: int, 
    db: Session = Depends(get_db)
):
    """
    Remove um formulário.
    """
    success = crud_formulario.delete_formulario(db, formulario_id=formulario_id)
    if not success:
        raise HTTPException(status_code=404, detail="Formulário não encontrado")
    return None
