# Thuanny Helen - Conftest para testes da API Monster Hunter

import pytest
import requests
from services.monster_service import MonsterService

@pytest.fixture(scope="session")
def base_url():
    """URL base da API."""
    return "https://mhw-db.com"

@pytest.fixture(scope="session")
def session():
    """
    Cria uma sessão de requisições reaproveitando a conexão TCP.
    """
    with requests.Session() as s:
        yield s

@pytest.fixture(scope="session")
def monster_service(session, base_url):
    """
    Fornece a instância do serviço de monstros para todos os testes.
    Isso centraliza a lógica de acesso à API.
    """
    return MonsterService(session, base_url)