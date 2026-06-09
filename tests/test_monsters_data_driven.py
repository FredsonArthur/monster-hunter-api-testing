# Fredson Arthur - Teste Data-Driven (Hunter Codex - Mockado)

import pytest
import json

@pytest.mark.parametrize("monster_name", [
    "Great Jagras", 
    "Kulu-Ya-Ku", 
    "Pukei-Pukei", 
    "Barroth", 
    "Anjanath"
])
def test_search_multiple_monsters(monster_service, mocker, monster_name):
    """
    Busca múltiplos monstros utilizando o Mocker para interceptar as chamadas.
    """
    # Configuramos o mock para interceptar a requisição de busca
    # O mocker aceita o parâmetro json para simular a resposta da API
    mock_response = [{"id": 1, "name": monster_name, "type": "large"}]
    
    # Registramos o mock para o endpoint de monstros
    mocker.get("https://mhw-db.com/monsters", json=mock_response)
    
    # Execução através do serviço
    response = monster_service.get_monster_by_name(monster_name)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == monster_name