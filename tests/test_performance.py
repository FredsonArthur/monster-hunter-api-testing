# Fredson Arthur - Teste de Performance da API Monster Hunter

import pytest
import time

def test_monster_endpoint_latency(base_url, session):
    """
    Valida se a resposta para o endpoint de monstros ocorre dentro 
    de um limite aceitável (ex: 800ms para considerar uma API responsiva).
    """
    threshold = 1.5  # limite em segundos
    
    start_time = time.perf_counter()
    response = session.get(f"{base_url}/monsters")
    end_time = time.perf_counter()
    
    duration = end_time - start_time

    print(f"\n[INFO] Tempo de resposta: {duration:.4f}s") # O pytest exibirá isso se rodar com -s
    
    assert response.status_code == 200
    assert duration < threshold, f"A API demorou {duration:.4f}s, acima do limite de {threshold}s"