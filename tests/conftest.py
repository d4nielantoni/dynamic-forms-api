import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db
from app.models.models import Formulario, Pergunta, OpcaoResposta, OpcoesRespostas

# Configuração do banco de dados de teste
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="function")
def test_db():
    """
    Fixture para criar um banco de dados de teste temporário.
    Cria as tabelas antes de cada teste e as remove após o teste.
    """
    engine = create_engine(
        TEST_SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Sobrescreve a dependência get_db para usar o banco de dados de teste
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Retorna a sessão do banco de dados para uso nos testes
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("./test.db"):
            os.remove("./test.db")

@pytest.fixture(scope="function")
def client(test_db):
    """
    Fixture para criar um cliente de teste para a API.
    """
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def seed_db(test_db):
    """
    Fixture para popular o banco de dados com dados de teste.
    """
    # Criar formulários de teste
    form1 = Formulario(
        titulo="Formulário de Teste 1",
        descricao="Descrição do formulário de teste 1",
        ordem=1
    )
    form2 = Formulario(
        titulo="Formulário de Teste 2",
        descricao="Descrição do formulário de teste 2",
        ordem=2
    )
    test_db.add(form1)
    test_db.add(form2)
    test_db.commit()
    test_db.refresh(form1)
    test_db.refresh(form2)
    
    # Criar perguntas de teste para o formulário 1
    pergunta1 = Pergunta(
        id_formulario=form1.id,
        titulo="Pergunta Sim/Não",
        codigo="sim_nao",
        orientacao_resposta="Responda sim ou não",
        ordem=1,
        obrigatoria=True,
        sub_pergunta=False,
        tipo_pergunta="Sim_Não"
    )
    
    pergunta2 = Pergunta(
        id_formulario=form1.id,
        titulo="Pergunta de Escolha Única",
        codigo="escolha_unica",
        orientacao_resposta="Escolha uma opção",
        ordem=2,
        obrigatoria=True,
        sub_pergunta=False,
        tipo_pergunta="unica_escolha"
    )
    
    pergunta3 = Pergunta(
        id_formulario=form1.id,
        titulo="Pergunta de Múltipla Escolha",
        codigo="multipla_escolha",
        orientacao_resposta="Escolha uma ou mais opções",
        ordem=3,
        obrigatoria=False,
        sub_pergunta=False,
        tipo_pergunta="multipla_escola"
    )
    
    test_db.add(pergunta1)
    test_db.add(pergunta2)
    test_db.add(pergunta3)
    test_db.commit()
    test_db.refresh(pergunta2)
    test_db.refresh(pergunta3)
    
    # Criar opções de resposta para a pergunta de escolha única
    opcoes_unica = [
        OpcoesRespostas(
            id_pergunta=pergunta2.id,
            resposta="Opção 1",
            ordem=1,
            resposta_aberta=False
        ),
        OpcoesRespostas(
            id_pergunta=pergunta2.id,
            resposta="Opção 2",
            ordem=2,
            resposta_aberta=False
        ),
        OpcoesRespostas(
            id_pergunta=pergunta2.id,
            resposta="Outra",
            ordem=3,
            resposta_aberta=True
        )
    ]
    
    # Criar opções de resposta para a pergunta de múltipla escolha
    opcoes_multipla = [
        OpcoesRespostas(
            id_pergunta=pergunta3.id,
            resposta="Opção A",
            ordem=1,
            resposta_aberta=False
        ),
        OpcoesRespostas(
            id_pergunta=pergunta3.id,
            resposta="Opção B",
            ordem=2,
            resposta_aberta=False
        ),
        OpcoesRespostas(
            id_pergunta=pergunta3.id,
            resposta="Opção C",
            ordem=3,
            resposta_aberta=False
        )
    ]
    
    test_db.add_all(opcoes_unica)
    test_db.add_all(opcoes_multipla)
    test_db.commit()
    
    return {
        "formularios": [form1, form2],
        "perguntas": [pergunta1, pergunta2, pergunta3]
    }
