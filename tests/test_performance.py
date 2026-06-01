# Fredson Arthur - Teste de Performance da API Monster Hunter

import pytest
import time

def test_monster_endpoint_latency(monster_service):
    """
    Valida se a resposta para o endpoint de monstros ocorre dentro 
    de um limite aceitável (ex: 1.5s para considerar uma API responsiva),
    utilizando a Service Layer para a requisição.
    """
    threshold = 2.5  # limite em segundos
    
    # Início da contagem
    start_time = time.perf_counter()
    
    # Execução através do serviço
    response = monster_service.get_all_monsters()
    
    # Fim da contagem
    end_time = time.perf_counter()
    
    duration = end_time - start_time

    # O pytest exibirá este print se rodar com o parâmetro -s
    print(f"\n[INFO] Tempo de resposta: {duration:.4f}s") 
    
    # Validações
    assert response.status_code == 200
    assert duration < threshold, f"A API demorou {duration:.4f}s, acima do limite de {threshold}s"