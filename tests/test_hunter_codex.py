import pytest
import json

RECURSOS = ["ailments", "armor", "items", "monsters", "weapons"]

@pytest.mark.parametrize("recurso", RECURSOS)
def test_mock_generic_resource_integrity(recurso, monster_service, mocker):
    """
    Valida de forma genérica se o recurso carregado possui dados consistentes.
    """
    caminho_arquivo = f"tests/fixtures/{recurso}.json"
    
    with open(caminho_arquivo, 'r') as f:
        mock_data = json.load(f)
    
    # Registra o mock para o endpoint genérico
    mocker.get(f"https://mhw-db.com/{recurso}", json=mock_data)
    
    # Execução através do serviço
    # Este método mantém o retorno do tipo 'Response'
    response = monster_service.get_resource(recurso)
    
    # Validações
    assert response.status_code == 200
    dados = response.json()
    
    assert isinstance(dados, list), f"O recurso {recurso} deveria retornar uma lista."
    assert len(dados) > 0, f"O arquivo de mock para {recurso} está vazio!"
    
    # Verifica se o primeiro item possui um ID (padrão da API MHW)
    if len(dados) > 0:
        assert "id" in dados[0], f"O objeto em {recurso} não possui a chave 'id'."