# Eduarda Santos - Teste Negativo para Busca de Monstros na API Monster Hunter

import pytest

def test_get_nonexistent_monster(monster_service):
    """
    Valida que a API retorna erro 404 ao buscar um ID inexistente,
    utilizando a Service Layer para a requisição.
    """
    monster_id = 99999
    
    # Execução através do serviço
    response = monster_service.get_monster_by_id(monster_id)
    
    # Validações
    assert response.status_code == 404
    
    # Valida a estrutura de erro retornada pela API
    error_data = response.json()
    assert "detail" in error_data
    assert error_data["detail"] == "Not Found"
    assert error_data["status"] == 404