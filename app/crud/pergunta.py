from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import List, Optional, Dict, Any
from app.models.models import Pergunta, OpcaoResposta, OpcoesRespostas
from app.schemas.pergunta import PerguntaCreate, PerguntaUpdate

def get_pergunta(db: Session, pergunta_id: int):
    """
    Obtém uma pergunta pelo ID
    """
    return db.query(Pergunta).filter(Pergunta.id == pergunta_id).first()

def get_perguntas(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    formulario_id: Optional[int] = None,
    tipo_pergunta: Optional[str] = None,
    obrigatoria: Optional[bool] = None,
    sub_pergunta: Optional[bool] = None,
    sort_by: str = "ordem",
    sort_order: str = "asc"
):
    """
    Obtém uma lista de perguntas com filtros, ordenação e paginação
    """
    query = db.query(Pergunta)
    
    # Aplicar filtros
    if formulario_id is not None:
        query = query.filter(Pergunta.id_formulario == formulario_id)
    
    if tipo_pergunta is not None:
        query = query.filter(Pergunta.tipo_pergunta == tipo_pergunta)
    
    if obrigatoria is not None:
        query = query.filter(Pergunta.obrigatoria == obrigatoria)
    
    if sub_pergunta is not None:
        query = query.filter(Pergunta.sub_pergunta == sub_pergunta)
    
    # Aplicar ordenação
    if sort_order.lower() == "desc":
        query = query.order_by(desc(getattr(Pergunta, sort_by)))
    else:
        query = query.order_by(asc(getattr(Pergunta, sort_by)))
    
    # Aplicar paginação
    return query.offset(skip).limit(limit).all()

def create_pergunta(db: Session, pergunta: PerguntaCreate):
    """
    Cria uma nova pergunta com opções de respostas múltiplas, se fornecidas
    """
    # Extrair opções de respostas múltiplas antes de criar a pergunta
    opcoes_data = None
    pergunta_dict = pergunta.model_dump()
    
    if 'opcoes_respostas_multiplas' in pergunta_dict and pergunta_dict['opcoes_respostas_multiplas']:
        opcoes_data = pergunta_dict.pop('opcoes_respostas_multiplas')
    
    # Criar a pergunta
    db_pergunta = Pergunta(**pergunta_dict)
    db.add(db_pergunta)
    db.commit()
    db.refresh(db_pergunta)
    
    # Adicionar opções de respostas múltiplas, se existirem
    if opcoes_data:
        for opcao in opcoes_data:
            db_opcao = OpcoesRespostas(
                id_pergunta=db_pergunta.id,
                resposta=opcao.get('resposta'),
                ordem=opcao.get('ordem', 0),
                resposta_aberta=opcao.get('resposta_aberta', False)
            )
            db.add(db_opcao)
        
        db.commit()
        db.refresh(db_pergunta)
    
    return db_pergunta

def update_pergunta(db: Session, pergunta_id: int, pergunta: PerguntaUpdate):
    """
    Atualiza uma pergunta existente
    """
    db_pergunta = get_pergunta(db, pergunta_id)
    if db_pergunta:
        update_data = pergunta.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_pergunta, key, value)
        db.commit()
        db.refresh(db_pergunta)
    return db_pergunta

def delete_pergunta(db: Session, pergunta_id: int):
    """
    Exclui uma pergunta pelo ID
    """
    db_pergunta = get_pergunta(db, pergunta_id)
    if db_pergunta:
        db.delete(db_pergunta)
        db.commit()
        return True
    return False

# Funções para opções de resposta
def create_opcao_resposta(db: Session, opcao_resposta_data: Dict[str, Any]):
    """
    Cria uma nova opção de resposta
    """
    db_opcao = OpcaoResposta(**opcao_resposta_data)
    db.add(db_opcao)
    db.commit()
    db.refresh(db_opcao)
    return db_opcao

def create_opcoes_respostas(db: Session, opcoes_respostas_data: Dict[str, Any]):
    """
    Cria uma nova opção de respostas múltiplas
    """
    db_opcoes = OpcoesRespostas(**opcoes_respostas_data)
    db.add(db_opcoes)
    db.commit()
    db.refresh(db_opcoes)
    return db_opcoes
