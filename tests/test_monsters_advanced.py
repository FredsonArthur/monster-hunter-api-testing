# Eduarda Santos - Teste Avançado de Busca de Monstros na API Monster Hunter

import pytest
import json
from jsonschema import validate

# Definição do schema esperado para um monstro (simplificado)
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

def test_search_monster_by_name_and_validate_schema(base_url, session):
    # Parâmetro de busca
    monster_name = "Great Jagras"
    params = {"q": json.dumps({"name": monster_name})}
    
    # Execução
    response = session.get(f"{base_url}/monsters", params=params)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    
    # Validando o Schema
    validate(instance=data, schema=MONSTER_SCHEMA)
    
    # Validando conteúdo específico
    assert len(data) > 0
    assert data[0]["name"] == monster_name