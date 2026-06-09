# Thuanny Helen - Teste de Saúde do Hunter Codex (Mockado)

import pytest

def test_api_is_reachable(monster_service, mocker):
    """
    Verifica se o serviço Hunter Codex está operando corretamente
    através de uma resposta mockada.
    """
    # Configuramos o mock para retornar uma lista com um monstro "saudável"
    mock_data = [{"id": 1, "name": "Great Jagras"}]
    mocker.get("https://mhw-db.com/monsters", json=mock_data)
    
    # Execução através do serviço
    response = monster_service.get_all_monsters()
    
    # Validações
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["name"] == "Great Jagras"