# Thuanny Helen - Teste de Saúde da API Monster Hunter

import pytest

def test_api_is_reachable(monster_service):
    """
    Verifica se a API está online e respondendo,
    utilizando a Service Layer para a requisição.
    """
    # Execução através do serviço
    response = monster_service.get_all_monsters()
    
    # Validações
    assert response.status_code == 200
    # Valida se recebemos pelo menos um item (a lista não deve estar vazia)
    assert len(response.json()) > 0