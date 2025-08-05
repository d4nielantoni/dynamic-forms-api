import pytest
import logging
from fastapi import status

# Configuração de logging para os testes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAPIFlow:
    """
    Testes de integração para verificar o fluxo completo da API.
    """
    
    def test_complete_form_flow(self, client):
        """
        Testa o fluxo completo de criação de um formulário com perguntas e opções,
        consulta, atualização e exclusão.
        """
        # 1. Criar um novo formulário
        logger.info("1. Criando um novo formulário")
        form_data = {
            "titulo": "Formulário de Integração",
            "descricao": "Teste de integração do fluxo completo",
            "ordem": 1
        }
        response = client.post("/api/v1/formularios/", json=form_data)
        assert response.status_code == status.HTTP_201_CREATED
        form = response.json()
        form_id = form["id"]
        logger.info(f"Formulário criado com ID: {form_id}")
        
        # 2. Criar uma pergunta de texto livre
        logger.info("2. Criando uma pergunta de texto livre")
        pergunta_texto = {
            "id_formulario": form_id,
            "titulo": "Qual seu nome completo?",
            "codigo": "nome_completo",
            "orientacao_resposta": "Digite seu nome completo",
            "ordem": 1,
            "obrigatoria": True,
            "sub_pergunta": False,
            "tipo_pergunta": "texto_livre"
        }
        response = client.post("/api/v1/perguntas/", json=pergunta_texto)
        assert response.status_code == status.HTTP_201_CREATED
        pergunta1 = response.json()
        pergunta1_id = pergunta1["id"]
        logger.info(f"Pergunta de texto criada com ID: {pergunta1_id}")
        
        # 3. Criar uma pergunta de escolha única com opções
        logger.info("3. Criando uma pergunta de escolha única com opções")
        pergunta_escolha = {
            "id_formulario": form_id,
            "titulo": "Qual sua faixa etária?",
            "codigo": "faixa_etaria",
            "orientacao_resposta": "Selecione sua faixa etária",
            "ordem": 2,
            "obrigatoria": True,
            "sub_pergunta": False,
            "tipo_pergunta": "unica_escolha",
            "opcoes_respostas_multiplas": [
                {
                    "resposta": "Até 18 anos",
                    "ordem": 1,
                    "resposta_aberta": False
                },
                {
                    "resposta": "19 a 30 anos",
                    "ordem": 2,
                    "resposta_aberta": False
                },
                {
                    "resposta": "31 a 50 anos",
                    "ordem": 3,
                    "resposta_aberta": False
                },
                {
                    "resposta": "Acima de 50 anos",
                    "ordem": 4,
                    "resposta_aberta": False
                }
            ]
        }
        response = client.post("/api/v1/perguntas/", json=pergunta_escolha)
        assert response.status_code == status.HTTP_201_CREATED
        pergunta2 = response.json()
        pergunta2_id = pergunta2["id"]
        logger.info(f"Pergunta de escolha única criada com ID: {pergunta2_id}")
        assert len(pergunta2["opcoes_respostas_multiplas"]) == 4
        
        # 4. Criar uma pergunta de múltipla escolha
        logger.info("4. Criando uma pergunta de múltipla escolha")
        pergunta_multipla = {
            "id_formulario": form_id,
            "titulo": "Quais redes sociais você utiliza?",
            "codigo": "redes_sociais",
            "orientacao_resposta": "Selecione todas as redes sociais que você utiliza",
            "ordem": 3,
            "obrigatoria": False,
            "sub_pergunta": False,
            "tipo_pergunta": "multipla_escola",
            "opcoes_respostas_multiplas": [
                {
                    "resposta": "Facebook",
                    "ordem": 1,
                    "resposta_aberta": False
                },
                {
                    "resposta": "Instagram",
                    "ordem": 2,
                    "resposta_aberta": False
                },
                {
                    "resposta": "Twitter",
                    "ordem": 3,
                    "resposta_aberta": False
                },
                {
                    "resposta": "LinkedIn",
                    "ordem": 4,
                    "resposta_aberta": False
                },
                {
                    "resposta": "Outra",
                    "ordem": 5,
                    "resposta_aberta": True
                }
            ]
        }
        response = client.post("/api/v1/perguntas/", json=pergunta_multipla)
        assert response.status_code == status.HTTP_201_CREATED
        pergunta3 = response.json()
        pergunta3_id = pergunta3["id"]
        logger.info(f"Pergunta de múltipla escolha criada com ID: {pergunta3_id}")
        assert len(pergunta3["opcoes_respostas_multiplas"]) == 5
        
        # 5. Listar todas as perguntas do formulário
        logger.info(f"5. Listando todas as perguntas do formulário {form_id}")
        response = client.get(f"/api/v1/perguntas/formulario/{form_id}")
        assert response.status_code == status.HTTP_200_OK
        perguntas = response.json()
        assert len(perguntas) == 3
        logger.info(f"Formulário possui {len(perguntas)} perguntas, como esperado")
        
        # 6. Filtrar perguntas por tipo
        logger.info("6. Filtrando perguntas por tipo")
        response = client.get(f"/api/v1/perguntas/formulario/{form_id}?tipo_pergunta=unica_escolha")
        assert response.status_code == status.HTTP_200_OK
        perguntas_filtradas = response.json()
        assert len(perguntas_filtradas) == 1
        assert perguntas_filtradas[0]["id"] == pergunta2_id
        logger.info("Filtro por tipo funcionou corretamente")
        
        # 7. Ordenar perguntas por ordem decrescente
        logger.info("7. Ordenando perguntas por ordem decrescente")
        response = client.get(f"/api/v1/perguntas/formulario/{form_id}?sort=ordem:desc")
        assert response.status_code == status.HTTP_200_OK
        perguntas_ordenadas = response.json()
        # Verificar se a lista está ordenada de forma decrescente
        ordens = [item["ordem"] for item in perguntas_ordenadas]
        assert ordens == sorted(ordens, reverse=True)
        logger.info("Ordenação por ordem decrescente funcionou corretamente")
        
        # 8. Atualizar uma pergunta
        logger.info(f"8. Atualizando a pergunta {pergunta1_id}")
        update_data = {
            "titulo": "Qual seu nome e sobrenome?",
            "orientacao_resposta": "Digite seu nome completo (nome e sobrenome)"
        }
        response = client.put(f"/api/v1/perguntas/{pergunta1_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        pergunta_atualizada = response.json()
        assert pergunta_atualizada["titulo"] == update_data["titulo"]
        assert pergunta_atualizada["orientacao_resposta"] == update_data["orientacao_resposta"]
        logger.info(f"Pergunta {pergunta1_id} atualizada com sucesso")
        
        # 9. Excluir uma pergunta
        logger.info(f"9. Excluindo a pergunta {pergunta3_id}")
        response = client.delete(f"/api/v1/perguntas/{pergunta3_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar se a pergunta foi excluída
        response = client.get(f"/api/v1/perguntas/formulario/{form_id}")
        assert response.status_code == status.HTTP_200_OK
        perguntas_restantes = response.json()
        assert len(perguntas_restantes) == 2
        ids_perguntas = [p["id"] for p in perguntas_restantes]
        assert pergunta3_id not in ids_perguntas
        logger.info(f"Pergunta {pergunta3_id} excluída com sucesso")
        
        # 10. Excluir o formulário
        logger.info(f"10. Excluindo o formulário {form_id}")
        response = client.delete(f"/api/v1/formularios/{form_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar se o formulário foi excluído
        response = client.get(f"/api/v1/formularios/{form_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        logger.info(f"Formulário {form_id} excluído com sucesso")
        
        logger.info("Teste de fluxo completo concluído com sucesso!")
