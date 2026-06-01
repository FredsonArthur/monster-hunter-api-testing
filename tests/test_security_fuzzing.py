#Eduarda Santos - Teste de Fuzzing para Busca de Monstros na API Monster Hunter

import pytest
import json

@pytest.mark.parametrize("invalid_query", [
    {"name": 12345},            # Nome como número (tipo inesperado)
    {"name": "'; DROP TABLE"},  # Tentativa básica de injeção
    {"name": "  "},             # Espaços em branco
    {"id": "abc"}               # ID como string em vez de número
])
def test_fuzzing_monster_search(base_url, session, invalid_query):
    """
    Testa como a API reage a inputs maliciosos ou incorretos.
    Esperamos que ela não retorne 500 (Internal Server Error).
    """
    params = {"q": json.dumps(invalid_query)}
    response = session.get(f"{base_url}/monsters", params=params)
    
    # Validação de segurança: 
    # A API deve nos devolver um erro de cliente (400) ou vazio (200), 
    # mas NUNCA um erro de servidor (500).
    assert response.status_code != 500, f"API falhou com erro 500 para input: {invalid_query}"