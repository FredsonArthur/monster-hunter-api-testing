# Eduarda Santos - Teste Avançado de Busca de Monstros (Hunter Codex - Mockado)

import pytest
import json
from jsonschema import validate

MONSTER_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"},
            "type": {"type": "string"}
        },
        "required": ["id", "name", "type"]
    }
}

def test_search_monster_by_name_and_validate_schema(monster_service, mocker):
    monster_name = "Great Jagras"
    mock_data = [{"id": 1, "name": "Great Jagras", "type": "large"}]
    
    # Removemos o match_querystring. O requests-mock tentará casar a URL.
    # Como o serviço monta a URL com query params (?q=...), 
    # podemos usar um matcher mais flexível:
    mocker.get("https://mhw-db.com/monsters", json=mock_data)
    
    # Execução através do serviço
    response = monster_service.get_monster_by_name(monster_name)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    
    validate(instance=data, schema=MONSTER_SCHEMA)
    assert len(data) > 0
    assert data[0]["name"] == monster_name