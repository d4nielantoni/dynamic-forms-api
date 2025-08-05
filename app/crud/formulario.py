from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.models import Formulario
from app.schemas.formulario import FormularioCreate, FormularioUpdate

def get_formulario(db: Session, formulario_id: int):
    """
    Obtém um formulário pelo ID
    """
    return db.query(Formulario).filter(Formulario.id == formulario_id).first()

def get_formularios(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtém uma lista de formulários com paginação
    """
    return db.query(Formulario).offset(skip).limit(limit).all()

def create_formulario(db: Session, formulario: FormularioCreate):
    """
    Cria um novo formulário
    """
    db_formulario = Formulario(**formulario.model_dump())
    db.add(db_formulario)
    db.commit()
    db.refresh(db_formulario)
    return db_formulario

def update_formulario(db: Session, formulario_id: int, formulario: FormularioUpdate):
    """
    Atualiza um formulário existente
    """
    db_formulario = get_formulario(db, formulario_id)
    if db_formulario:
        update_data = formulario.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_formulario, key, value)
        db.commit()
        db.refresh(db_formulario)
    return db_formulario

def delete_formulario(db: Session, formulario_id: int):
    """
    Exclui um formulário pelo ID e todas as suas perguntas relacionadas
    """
    from app.models.models import Pergunta
    
    # Verificar se o formulário existe
    db_formulario = get_formulario(db, formulario_id)
    if db_formulario:
        # Excluir todas as perguntas relacionadas ao formulário
        db.query(Pergunta).filter(Pergunta.id_formulario == formulario_id).delete()
        
        # Excluir o formulário
        db.delete(db_formulario)
        db.commit()
        return True
    return False
