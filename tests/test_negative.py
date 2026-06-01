# Eduarda Santos - Teste Negativo para Busca de Monstros na API Monster Hunter

import pytest

def test_get_nonexistent_monster(base_url, session):
    monster_id = 99999
    response = session.get(f"{base_url}/monsters/{monster_id}")
    
    # 1. Valida o status code (isso estava correto)
    assert response.status_code == 404
    
    # 2. Valida a estrutura real da API
    error_data = response.json()
    assert "detail" in error_data
    assert error_data["detail"] == "Not Found"
    assert error_data["status"] == 404