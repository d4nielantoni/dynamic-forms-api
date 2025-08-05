from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Formulario(Base):
    """
    Modelo para representar um formulário.
    """
    __tablename__ = "formulario"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    ordem = Column(Integer, default=0)
    
    # Relacionamento com perguntas
    perguntas = relationship("Pergunta", back_populates="formulario")

class Pergunta(Base):
    """
    Modelo para representar uma pergunta de um formulário.
    """
    __tablename__ = "pergunta"

    id = Column(Integer, primary_key=True, index=True)
    id_formulario = Column(Integer, ForeignKey("formulario.id"), nullable=False)
    titulo = Column(String(255), nullable=False)
    codigo = Column(String(100), nullable=True)
    orientacao_resposta = Column(Text, nullable=True)
    ordem = Column(Integer, default=0)
    obrigatoria = Column(Boolean, default=False)
    sub_pergunta = Column(Boolean, default=False)
    tipo_pergunta = Column(String(50), nullable=False)  # Sim_Não, multipla_escola, unica_escolha, texto_livre, Inteiro, Numero com duas casas decimais
    
    # Relacionamentos
    formulario = relationship("Formulario", back_populates="perguntas")
    opcoes_respostas = relationship("OpcaoResposta", back_populates="pergunta")
    opcoes_respostas_multiplas = relationship("OpcoesRespostas", back_populates="pergunta")

class OpcaoResposta(Base):
    """
    Modelo para representar as opções de resposta para uma pergunta.
    """
    __tablename__ = "opcoes_resposta_pergunta"

    id = Column(Integer, primary_key=True, index=True)
    id_opcao_resposta = Column(Integer, nullable=False)
    id_pergunta = Column(Integer, ForeignKey("pergunta.id"), nullable=False)
    
    # Relacionamento
    pergunta = relationship("Pergunta", back_populates="opcoes_respostas")

class OpcoesRespostas(Base):
    """
    Modelo para representar as respostas de opções múltiplas.
    """
    __tablename__ = "opcoes_respostas"

    id = Column(Integer, primary_key=True, index=True)
    id_pergunta = Column(Integer, ForeignKey("pergunta.id"), nullable=False)
    resposta = Column(Text, nullable=True)
    ordem = Column(Integer, default=0)
    resposta_aberta = Column(Boolean, default=False)
    
    # Relacionamento
    pergunta = relationship("Pergunta", back_populates="opcoes_respostas_multiplas")
