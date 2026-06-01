# Fredson Arthur - Teste Data-Driven para Busca de Monstros na API Monster Hunter

import pytest
import json

@pytest.mark.parametrize("monster_name", [
    "Great Jagras", 
    "Kulu-Ya-Ku", 
    "Pukei-Pukei", 
    "Barroth", 
    "Anjanath"
])
def test_search_multiple_monsters(base_url, session, monster_name):
    params = {"q": json.dumps({"name": monster_name})}
    response = session.get(f"{base_url}/monsters", params=params)
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) > 0
    # Validamos que o nome retornado é exatamente o que buscamos
    assert data[0]["name"] == monster_name