# Thuanny Helen - Teste de Saúde da API Monster Hunter

import pytest

def test_api_is_reachable(base_url, session):
    """
    Verifica se a API está online e respondendo.
    """
    response = session.get(f"{base_url}/monsters")
    assert response.status_code == 200
    # Valida se recebemos pelo menos um item (a lista não deve estar vazia)
    assert len(response.json()) > 0