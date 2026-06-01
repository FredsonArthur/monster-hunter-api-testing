# Thuanny Helen - Conftest para testes da API Monster Hunter

import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    # URL base da API
    return "https://mhw-db.com"

@pytest.fixture(scope="session")
def session():
    """
    Cria uma sessão de requisições. 
    Usar 'session' é uma boa prática pois reaproveita a conexão TCP,
    tornando os testes mais rápidos.
    """
    with requests.Session() as s:
        # Podemos definir headers padrão aqui, se a API exigisse autenticação
        # s.headers.update({"Accept": "application/json"})
        yield s

def test_get_specific_monster(base_url, session):
    monster_id = 1
    # Montamos a URL concatenando o endpoint
    url = f"{base_url}/monsters/{monster_id}"
    
    # Realizamos o GET
    response = session.get(url)
    
    # Validações iniciais de conexão
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == monster_id
    assert "name" in data