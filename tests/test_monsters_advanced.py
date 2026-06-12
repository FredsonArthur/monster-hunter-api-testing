# Eduarda Santos - Teste Avançado de Busca de Monstros (Hunter Codex - Mockado)

import pytest
import json
from jsonschema import validate

MONSTER_SCHEMA = {
    "type": "object", # Alterado de "array" para "object", pois o serviço retorna o primeiro item do dict
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
        "type": {"type": "string"}
    },
    "required": ["id", "name", "type"]
}

def test_search_monster_by_name_and_validate_schema(monster_service, mocker):
    monster_name = "Great Jagras"
    mock_data = [{"id": 1, "name": "Great Jagras", "type": "large"}]
    
    # O mocker intercepta a chamada que o service fará internamente
    mocker.get("https://mhw-db.com/monsters", json=mock_data)
    
    # Execução através do serviço
    # O resultado agora é o dicionário do monstro
    data = monster_service.get_monster_by_name(monster_name)
    
    # Assertions
    assert data is not None
    validate(instance=data, schema=MONSTER_SCHEMA)
    assert data["name"] == monster_name