# Thuanny Helen - Conftest para testes da API Monster Hunter (Hunter Codex)

import pytest
import requests
import requests_mock
from unittest.mock import MagicMock
from services.monster_service import MonsterService

@pytest.fixture(scope="session")
def base_url():
    """URL base da API."""
    return "https://mhw-db.com"

@pytest.fixture(scope="session")
def session():
    """Cria uma sessão de requisições."""
    with requests.Session() as s:
        yield s

@pytest.fixture(scope="function")
def mocker():
    """Fornece o objeto de mock para interceptar chamadas HTTP."""
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture(scope="function")
def mock_collection():
    """Cria um mock para a coleção do MongoDB que retorna None (cache vazio)."""
    mock = MagicMock()
    # Força o find_one a retornar None, indicando que não há nada no banco
    mock.find_one.return_value = None
    return mock

@pytest.fixture(scope="function")
def monster_service(session, base_url, mocker, mock_collection):
    """
    Fornece a instância do serviço de monstros.
    Injeta o 'mock_collection' para evitar conexão com o banco real.
    """
    return MonsterService(session, base_url, collection=mock_collection)