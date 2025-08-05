from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.models.models import Formulario, Pergunta, OpcoesRespostas

# Recria as tabelas
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed_data():
    try:
        # Criar formulários de exemplo
        form1 = Formulario(
            titulo="Pesquisa de Satisfação",
            descricao="Formulário para avaliar a satisfação dos clientes",
            ordem=1
        )
        
        form2 = Formulario(
            titulo="Cadastro de Usuário",
            descricao="Formulário para cadastro de novos usuários",
            ordem=2
        )
        
        db.add(form1)
        db.add(form2)
        db.commit()
        
        # Criar perguntas para o formulário 1
        perguntas_form1 = [
            Pergunta(
                id_formulario=1,
                titulo="Você está satisfeito com nosso serviço?",
                codigo="satisfacao",
                orientacao_resposta="Escolha uma opção",
                ordem=1,
                obrigatoria=True,
                tipo_pergunta="Sim_Não"
            ),
            Pergunta(
                id_formulario=1,
                titulo="Como você avalia nosso atendimento?",
                codigo="avaliacao",
                orientacao_resposta="Escolha uma das opções abaixo",
                ordem=2,
                obrigatoria=True,
                tipo_pergunta="unica_escolha"
            ),
            Pergunta(
                id_formulario=1,
                titulo="Quais serviços você utilizou?",
                codigo="servicos",
                orientacao_resposta="Selecione todos os serviços utilizados",
                ordem=3,
                obrigatoria=False,
                tipo_pergunta="multipla_escola"
            ),
            Pergunta(
                id_formulario=1,
                titulo="Deixe um comentário ou sugestão",
                codigo="comentario",
                orientacao_resposta="Escreva seu comentário",
                ordem=4,
                obrigatoria=False,
                tipo_pergunta="texto_livre"
            )
        ]
        
        # Criar perguntas para o formulário 2
        perguntas_form2 = [
            Pergunta(
                id_formulario=2,
                titulo="Nome completo",
                codigo="nome",
                orientacao_resposta="Digite seu nome completo",
                ordem=1,
                obrigatoria=True,
                tipo_pergunta="texto_livre"
            ),
            Pergunta(
                id_formulario=2,
                titulo="Idade",
                codigo="idade",
                orientacao_resposta="Digite sua idade",
                ordem=2,
                obrigatoria=True,
                tipo_pergunta="Inteiro"
            ),
            Pergunta(
                id_formulario=2,
                titulo="Você aceita receber notificações?",
                codigo="notificacoes",
                orientacao_resposta="Escolha uma opção",
                ordem=3,
                obrigatoria=True,
                tipo_pergunta="Sim_Não"
            )
        ]
        
        for pergunta in perguntas_form1 + perguntas_form2:
            db.add(pergunta)
        
        db.commit()
        
        # Adicionar opções de resposta para a pergunta de avaliação
        opcoes_avaliacao = [
            OpcoesRespostas(id_pergunta=2, resposta="Excelente", ordem=1),
            OpcoesRespostas(id_pergunta=2, resposta="Bom", ordem=2),
            OpcoesRespostas(id_pergunta=2, resposta="Regular", ordem=3),
            OpcoesRespostas(id_pergunta=2, resposta="Ruim", ordem=4),
            OpcoesRespostas(id_pergunta=2, resposta="Péssimo", ordem=5)
        ]
        
        # Adicionar opções de resposta para a pergunta de serviços
        opcoes_servicos = [
            OpcoesRespostas(id_pergunta=3, resposta="Atendimento ao cliente", ordem=1),
            OpcoesRespostas(id_pergunta=3, resposta="Suporte técnico", ordem=2),
            OpcoesRespostas(id_pergunta=3, resposta="Vendas", ordem=3),
            OpcoesRespostas(id_pergunta=3, resposta="Pós-venda", ordem=4),
            OpcoesRespostas(id_pergunta=3, resposta="Outro", ordem=5, resposta_aberta=True)
        ]
        
        for opcao in opcoes_avaliacao + opcoes_servicos:
            db.add(opcao)
        
        db.commit()
        
        print("Dados de exemplo inseridos com sucesso!")
        
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
