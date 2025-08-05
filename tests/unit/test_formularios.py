import pytest
import logging
from fastapi import status
from app.schemas.formulario import FormularioCreate, FormularioUpdate

# Configuração de logging para os testes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestFormularioEndpoints:
    """
    Testes para os endpoints de formulários.
    """
    
    def test_get_all_formularios(self, client, seed_db):
        """
        Testa o endpoint para obter todos os formulários.
        """
        logger.info("Testando obtenção de todos os formulários")
        response = client.get("/api/v1/formularios/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        assert data[0]["titulo"] == "Formulário de Teste 1"
        assert data[1]["titulo"] == "Formulário de Teste 2"
        logger.info(f"Formulários obtidos com sucesso: {len(data)} formulários encontrados")
    
    def test_get_formulario_by_id(self, client, seed_db):
        """
        Testa o endpoint para obter um formulário pelo ID.
        """
        formulario_id = seed_db["formularios"][0].id
        logger.info(f"Testando obtenção do formulário com ID {formulario_id}")
        response = client.get(f"/api/v1/formularios/{formulario_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == formulario_id
        assert data["titulo"] == "Formulário de Teste 1"
        logger.info(f"Formulário {formulario_id} obtido com sucesso")
    
    def test_get_formulario_not_found(self, client):
        """
        Testa o endpoint para obter um formulário que não existe.
        """
        formulario_id = 999
        logger.info(f"Testando obtenção de formulário inexistente com ID {formulario_id}")
        response = client.get(f"/api/v1/formularios/{formulario_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        logger.info(f"Formulário {formulario_id} não encontrado, como esperado")
    
    def test_create_formulario(self, client):
        """
        Testa o endpoint para criar um novo formulário.
        """
        formulario_data = {
            "titulo": "Novo Formulário",
            "descricao": "Descrição do novo formulário",
            "ordem": 3
        }
        logger.info(f"Testando criação de formulário: {formulario_data}")
        response = client.post("/api/v1/formularios/", json=formulario_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["titulo"] == formulario_data["titulo"]
        assert data["descricao"] == formulario_data["descricao"]
        assert data["ordem"] == formulario_data["ordem"]
        assert "id" in data
        logger.info(f"Formulário criado com sucesso com ID {data['id']}")
    
    def test_update_formulario(self, client, seed_db):
        """
        Testa o endpoint para atualizar um formulário existente.
        """
        formulario_id = seed_db["formularios"][0].id
        update_data = {
            "titulo": "Formulário Atualizado",
            "descricao": "Descrição atualizada",
            "ordem": 10
        }
        logger.info(f"Testando atualização do formulário {formulario_id}: {update_data}")
        response = client.put(f"/api/v1/formularios/{formulario_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == formulario_id
        assert data["titulo"] == update_data["titulo"]
        assert data["descricao"] == update_data["descricao"]
        assert data["ordem"] == update_data["ordem"]
        logger.info(f"Formulário {formulario_id} atualizado com sucesso")
    
    def test_update_formulario_not_found(self, client):
        """
        Testa o endpoint para atualizar um formulário que não existe.
        """
        formulario_id = 999
        update_data = {
            "titulo": "Formulário Inexistente",
            "descricao": "Descrição atualizada",
            "ordem": 10
        }
        logger.info(f"Testando atualização de formulário inexistente com ID {formulario_id}")
        response = client.put(f"/api/v1/formularios/{formulario_id}", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        logger.info(f"Formulário {formulario_id} não encontrado para atualização, como esperado")
    
    def test_delete_formulario(self, client, seed_db):
        """
        Testa o endpoint para excluir um formulário.
        """
        formulario_id = seed_db["formularios"][0].id
        logger.info(f"Testando exclusão do formulário com ID {formulario_id}")
        response = client.delete(f"/api/v1/formularios/{formulario_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar se o formulário foi realmente excluído
        get_response = client.get(f"/api/v1/formularios/{formulario_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
        logger.info(f"Formulário {formulario_id} excluído com sucesso")
    
    def test_delete_formulario_not_found(self, client):
        """
        Testa o endpoint para excluir um formulário que não existe.
        """
        formulario_id = 999
        logger.info(f"Testando exclusão de formulário inexistente com ID {formulario_id}")
        response = client.delete(f"/api/v1/formularios/{formulario_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        logger.info(f"Formulário {formulario_id} não encontrado para exclusão, como esperado")
