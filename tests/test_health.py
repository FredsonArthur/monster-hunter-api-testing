# Thuanny Helen - Teste de Saúde do Hunter Codex (Mockado)

import pytest

def test_api_is_reachable(monster_service, mocker):
    """
    Verifica se o serviço Hunter Codex está operando corretamente
    através de uma resposta mockada.
    """
    # 1. Configuramos o mock para retornar uma lista com um monstro "saudável"
    # O mocker intercepta a chamada que o service fará internamente
    mock_data = [{"id": 1, "name": "Great Jagras"}]
    mocker.get("https://mhw-db.com/monsters", json=mock_data)
    
    # 2. Execução através do serviço
    # get_all_monsters ainda retorna o objeto Response, 
    # então o assert de status_code aqui permanece válido.
    response = monster_service.get_all_monsters()
    
    # 3. Validações
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Great Jagras"