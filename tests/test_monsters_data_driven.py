# Fredson Arthur - Teste Data-Driven para Busca de Monstros na API Monster Hunter

import pytest

@pytest.mark.parametrize("monster_name", [
    "Great Jagras", 
    "Kulu-Ya-Ku", 
    "Pukei-Pukei", 
    "Barroth", 
    "Anjanath"
])
def test_search_multiple_monsters(monster_service, monster_name):
    """
    Busca múltiplos monstros utilizando a Service Layer para 
    abstrair a complexidade da requisição.
    """
    # Execução através do serviço
    response = monster_service.get_monster_by_name(monster_name)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) > 0
    # Validamos que o nome retornado é exatamente o que buscamos
    assert data[0]["name"] == monster_name