# Eduarda Santos - Teste Negativo para Busca de Monstros (Hunter Codex - Mockado)

import pytest

def test_get_nonexistent_monster(monster_service, mocker):
    """
    Valida que o serviço trata o erro 404, 
    sem necessidade de conexão com a API real.
    """
    monster_id = 99999
    
    # 1. Configuramos o Mocker para simular a falha 404
    mocker.get(
        f"https://mhw-db.com/monsters/{monster_id}", 
        status_code=404, 
        json={"detail": "Not Found", "status": 404}
    )
    
    # 2. Execução através do serviço
    # O método get_monster_by_id retorna um objeto Response,
    # por isso o status_code continua sendo validado aqui.
    response = monster_service.get_monster_by_id(monster_id)
    
    # 3. Validações
    assert response.status_code == 404
    error_data = response.json()
    assert error_data["detail"] == "Not Found"
    assert error_data["status"] == 404