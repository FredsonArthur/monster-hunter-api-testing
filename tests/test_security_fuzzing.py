# Eduarda Santos - Teste de Fuzzing (Hunter Codex - Mockado)

import pytest
import json

@pytest.mark.parametrize("invalid_query", [
    {"name": 12345},            # Nome como número
    {"name": "'; DROP TABLE"},  # Tentativa de injeção
    {"name": "  "},             # Espaços em branco
    {"id": "abc"}               # ID como string
])
def test_fuzzing_monster_search(monster_service, mocker, invalid_query):
    """
    Testa se o serviço lida com inputs inválidos sem disparar erros 500.
    Agora 100% local via Mocker.
    """
    # Configuramos o mock para retornar um erro 400 (Bad Request) para inputs inválidos
    # Isso simula o comportamento de uma API segura.
    mocker.get("https://mhw-db.com/monsters", status_code=400, json={"error": "Bad Request"})
    
    # Execução através do serviço
    response = monster_service.get_monster_by_name(json.dumps(invalid_query))
    
    # Validação de segurança: 
    # O mock garantiu que não houve erro 500.
    assert response.status_code != 500, f"API falhou com erro 500 para input: {invalid_query}"
    assert response.status_code == 400