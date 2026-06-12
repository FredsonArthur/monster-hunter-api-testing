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
    Agora 100% local via Mocker e validando o retorno None do serviço.
    """
    # 1. Configuramos o mock para retornar um erro 400 (Bad Request)
    mocker.get("https://mhw-db.com/monsters", status_code=400, json={"error": "Bad Request"})
    
    # 2. Execução através do serviço
    # O serviço retorna None quando a API retorna erro (status_code != 200)
    result = monster_service.get_monster_by_name(json.dumps(invalid_query))
    
    # 3. Validação de segurança: 
    # O serviço deve retornar None, garantindo que não houve estouro (500)
    assert result is None, f"O serviço deveria retornar None para input inválido: {invalid_query}"