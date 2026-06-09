# Thuanny Helen - Conftest para testes da API Monster Hunter (Hunter Codex)

import pytest
import requests
import requests_mock
from services.monster_service import MonsterService

@pytest.fixture(scope="session")
def base_url():
    """URL base da API (mantida para referência)."""
    return "https://mhw-db.com"

@pytest.fixture(scope="session")
def session():
    """
    Cria uma sessão de requisições reaproveitando a conexão TCP.
    """
    with requests.Session() as s:
        yield s

@pytest.fixture(scope="function")
def mocker():
    """
    Fornece o objeto de mock para interceptar as chamadas HTTP.
    Usamos scope='function' para garantir que um teste não interfira no outro.
    """
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture(scope="function")
def monster_service(session, base_url, mocker):
    """
    Fornece a instância do serviço de monstros.
    Agora, o serviço utilizará o 'mocker' para interceptar chamadas.
    """
    return MonsterService(session, base_url)