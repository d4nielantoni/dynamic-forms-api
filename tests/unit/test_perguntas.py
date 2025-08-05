import pytest
import logging
from fastapi import status
from app.schemas.pergunta import PerguntaCreate, PerguntaUpdate

# Configuração de logging para os testes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestPerguntaEndpoints:
    """
    Testes para os endpoints de perguntas.
    """
    
    def test_get_all_perguntas(self, client, seed_db):
        """
        Testa o endpoint para obter todas as perguntas.
        """
        logger.info("Testando obtenção de todas as perguntas")
        response = client.get("/api/v1/perguntas/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        logger.info(f"Perguntas obtidas com sucesso: {len(data)} perguntas encontradas")
    
    def test_get_pergunta_by_id(self, client, seed_db):
        """
        Testa o endpoint para obter uma pergunta pelo ID.
        """
        pergunta_id = seed_db["perguntas"][0].id
        logger.info(f"Testando obtenção da pergunta com ID {pergunta_id}")
        response = client.get(f"/api/v1/perguntas/{pergunta_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == pergunta_id
        assert data["titulo"] == "Pergunta Sim/Não"
        logger.info(f"Pergunta {pergunta_id} obtida com sucesso")
    
    def test_get_pergunta_not_found(self, client):
        """
        Testa o endpoint para obter uma pergunta que não existe.
        """
        pergunta_id = 999
        logger.info(f"Testando obtenção de pergunta inexistente com ID {pergunta_id}")
        response = client.get(f"/api/v1/perguntas/{pergunta_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        logger.info(f"Pergunta {pergunta_id} não encontrada, como esperado")
    
    def test_create_pergunta(self, client, seed_db):
        """
        Testa o endpoint para criar uma nova pergunta.
        """
        formulario_id = seed_db["formularios"][0].id
        pergunta_data = {
            "id_formulario": formulario_id,
            "titulo": "Nova Pergunta",
            "codigo": "nova_pergunta",
            "orientacao_resposta": "Responda a nova pergunta",
            "ordem": 4,
            "obrigatoria": True,
            "sub_pergunta": False,
            "tipo_pergunta": "texto_livre"
        }
        logger.info(f"Testando criação de pergunta: {pergunta_data}")
        response = client.post("/api/v1/perguntas/", json=pergunta_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["titulo"] == pergunta_data["titulo"]
        assert data["codigo"] == pergunta_data["codigo"]
        assert data["id_formulario"] == formulario_id
        assert "id" in data
        logger.info(f"Pergunta criada com sucesso com ID {data['id']}")
    
    def test_create_pergunta_with_opcoes(self, client, seed_db):
        """
        Testa o endpoint para criar uma nova pergunta com opções de resposta.
        """
        formulario_id = seed_db["formularios"][0].id
        pergunta_data = {
            "id_formulario": formulario_id,
            "titulo": "Pergunta com Opções",
            "codigo": "pergunta_opcoes",
            "orientacao_resposta": "Escolha uma opção",
            "ordem": 5,
            "obrigatoria": True,
            "sub_pergunta": False,
            "tipo_pergunta": "unica_escolha",
            "opcoes_respostas_multiplas": [
                {
                    "resposta": "Opção A",
                    "ordem": 1,
                    "resposta_aberta": False
                },
                {
                    "resposta": "Opção B",
                    "ordem": 2,
                    "resposta_aberta": False
                }
            ]
        }
        logger.info(f"Testando criação de pergunta com opções: {pergunta_data}")
        response = client.post("/api/v1/perguntas/", json=pergunta_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["titulo"] == pergunta_data["titulo"]
        assert len(data["opcoes_respostas_multiplas"]) == 2
        logger.info(f"Pergunta com opções criada com sucesso com ID {data['id']}")
    
    def test_update_pergunta(self, client, seed_db):
        """
        Testa o endpoint para atualizar uma pergunta existente.
        """
        pergunta_id = seed_db["perguntas"][0].id
        update_data = {
            "titulo": "Pergunta Atualizada",
            "codigo": "pergunta_atualizada",
            "orientacao_resposta": "Orientação atualizada",
            "ordem": 10,
            "obrigatoria": False
        }
        logger.info(f"Testando atualização da pergunta {pergunta_id}: {update_data}")
        response = client.put(f"/api/v1/perguntas/{pergunta_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == pergunta_id
        assert data["titulo"] == update_data["titulo"]
        assert data["codigo"] == update_data["codigo"]
        assert data["obrigatoria"] == update_data["obrigatoria"]
        logger.info(f"Pergunta {pergunta_id} atualizada com sucesso")
    
    def test_update_pergunta_not_found(self, client):
        """
        Testa o endpoint para atualizar uma pergunta que não existe.
        """
        pergunta_id = 999
        update_data = {
            "titulo": "Pergunta Inexistente",
            "codigo": "pergunta_inexistente",
            "orientacao_resposta": "Orientação atualizada",
            "ordem": 10,
            "obrigatoria": False
        }
        logger.info(f"Testando atualização de pergunta inexistente com ID {pergunta_id}")
        response = client.put(f"/api/v1/perguntas/{pergunta_id}", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        logger.info(f"Pergunta {pergunta_id} não encontrada para atualização, como esperado")
    
    def test_delete_pergunta(self, client, seed_db):
        """
        Testa o endpoint para excluir uma pergunta.
        """
        pergunta_id = seed_db["perguntas"][0].id
        logger.info(f"Testando exclusão da pergunta com ID {pergunta_id}")
        response = client.delete(f"/api/v1/perguntas/{pergunta_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar se a pergunta foi realmente excluída
        get_response = client.get(f"/api/v1/perguntas/{pergunta_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
        logger.info(f"Pergunta {pergunta_id} excluída com sucesso")
    
    def test_delete_pergunta_not_found(self, client):
        """
        Testa o endpoint para excluir uma pergunta que não existe.
        """
        pergunta_id = 999
        logger.info(f"Testando exclusão de pergunta inexistente com ID {pergunta_id}")
        response = client.delete(f"/api/v1/perguntas/{pergunta_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        logger.info(f"Pergunta {pergunta_id} não encontrada para exclusão, como esperado")
    
    def test_get_perguntas_by_formulario(self, client, seed_db):
        """
        Testa o endpoint para obter perguntas de um formulário específico.
        """
        formulario_id = seed_db["formularios"][0].id
        logger.info(f"Testando obtenção de perguntas do formulário {formulario_id}")
        response = client.get(f"/api/v1/perguntas/formulario/{formulario_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        for pergunta in data:
            assert pergunta["id_formulario"] == formulario_id
        logger.info(f"Perguntas do formulário {formulario_id} obtidas com sucesso: {len(data)} perguntas encontradas")
    
    def test_get_perguntas_by_formulario_with_filters(self, client, seed_db):
        """
        Testa o endpoint para obter perguntas de um formulário com filtros.
        """
        formulario_id = seed_db["formularios"][0].id
        logger.info(f"Testando obtenção de perguntas do formulário {formulario_id} com filtros")
        
        # Filtrar por tipo_pergunta
        response = client.get(f"/api/v1/perguntas/formulario/{formulario_id}?tipo_pergunta=Sim_Não")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["tipo_pergunta"] == "Sim_Não"
        logger.info(f"Filtro por tipo_pergunta funcionou corretamente: {len(data)} perguntas encontradas")
        
        # Filtrar por obrigatoria
        response = client.get(f"/api/v1/perguntas/formulario/{formulario_id}?obrigatoria=true")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        for pergunta in data:
            assert pergunta["obrigatoria"] == True
        logger.info(f"Filtro por obrigatoria funcionou corretamente: {len(data)} perguntas encontradas")
        
        # Ordenar por ordem (desc)
        response = client.get(f"/api/v1/perguntas/formulario/{formulario_id}?sort=ordem:desc")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        # Verificar se a lista está ordenada de forma decrescente
        ordens = [item["ordem"] for item in data]
        assert ordens == sorted(ordens, reverse=True)
        logger.info("Ordenação por ordem (desc) funcionou corretamente")
        
        # Paginação
        response = client.get(f"/api/v1/perguntas/formulario/{formulario_id}?skip=1&limit=1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        logger.info("Paginação funcionou corretamente")
