import pytest
import time

def test_monster_endpoint_latency(monster_service, mocker):
    """
    Testa a latência do endpoint de monstros utilizando o Mocker para interceptar.
    """
    # Registramos o mock antes de chamar o serviço
    mocker.get("https://mhw-db.com/monsters", json=[{"id": 1, "name": "Great Jagras"}])
    
    threshold = 2.5
    start_time = time.perf_counter()
    
    # Este método mantém o retorno original como 'Response'
    response = monster_service.get_all_monsters()
    
    end_time = time.perf_counter()
    duration = end_time - start_time

    # Asserções validadas contra o objeto Response
    assert response.status_code == 200
    assert duration < threshold