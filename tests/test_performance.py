import pytest
import time

def test_monster_endpoint_latency(monster_service, mocker):
    # Registramos o mock antes de chamar o serviço
    mocker.get("https://mhw-db.com/monsters", json=[{"id": 1, "name": "Great Jagras"}])
    
    threshold = 2.5
    start_time = time.perf_counter()
    
    response = monster_service.get_all_monsters()
    
    end_time = time.perf_counter()
    duration = end_time - start_time

    assert response.status_code == 200
    assert duration < threshold