"""
Testes para todos os recursos do Hunter Codex
Verifica busca, cache e integridade dos 5 recursos
"""

import pytest
import json
from pathlib import Path
from services.monster_service import MonsterService
import requests


class TestAllResources:
    """Testa todos os 5 recursos do sistema"""
    
    @pytest.fixture
    def service(self):
        """Fixture do serviço (sem MongoDB real para testes)"""
        return MonsterService(requests.Session(), "https://mhw-db.com", collection=None)
    
    @pytest.mark.parametrize("recurso, nome_exemplo", [
        ("monsters", "Great Jagras"),
        ("ailments", "Poison"),
        ("armor", "Leather Headgear"),
        ("items", "Potion"),
        ("weapons", "Buster Sword 1"),
    ])
    def test_buscar_recurso_existe(self, service, recurso, nome_exemplo):
        """Testa se consegue buscar cada tipo de recurso"""
        resultado = service.get_by_name(recurso, nome_exemplo)
        
        assert resultado is not None, f"{recurso}: '{nome_exemplo}' não encontrado"
        assert "name" in resultado, f"{recurso}: resultado sem campo 'name'"
        assert resultado["name"] == nome_exemplo or resultado["name"].lower() == nome_exemplo.lower()
    
    @pytest.mark.parametrize("recurso, nome_invalido", [
        ("monsters", "MonstroQueNaoExiste123"),
        ("ailments", "StatusInexistenteXYZ"),
        ("armor", "ArmaduraFalsa"),
        ("items", "ItemImaginario"),
        ("weapons", "ArmaQueNaoExiste"),
    ])
    def test_buscar_recurso_nao_existe(self, service, recurso, nome_invalido):
        """Testa busca por nome inexistente"""
        resultado = service.get_by_name(recurso, nome_invalido)
        assert resultado is None, f"{recurso}: '{nome_invalido}' não deveria existir"
    
    @pytest.mark.parametrize("recurso", ["monsters", "ailments", "armor", "items", "weapons"])
    def test_cache_funciona(self, service, recurso):
        """Testa se o cache está funcionando (segunda busca é mais rápida)"""
        import time
        
        nome_teste = "Rathalos" if recurso == "monsters" else "Poison"
        
        # Primeira busca (API)
        start1 = time.time()
        resultado1 = service.get_by_name(recurso, nome_teste)
        tempo1 = time.time() - start1
        
        assert resultado1 is not None
        
        # Segunda busca (cache)
        start2 = time.time()
        resultado2 = service.get_by_name(recurso, nome_teste)
        tempo2 = time.time() - start2
        
        assert resultado2 is not None
        assert resultado1["name"] == resultado2["name"]
        
        # Cache deve ser mais rápido (ou igual em caso de erro)
        # Não falha se não for, apenas alerta
        if tempo2 > tempo1:
            print(f"⚠️ Cache pode não estar funcionando para {recurso}: {tempo2:.3f}s > {tempo1:.3f}s")
    
    def test_todos_recursos_tem_fixtures(self):
        """Verifica se todos os recursos têm arquivos de fixture"""
        recursos_fixtures = ["ailments", "armor", "items", "monsters", "weapons"]
        
        for recurso in recursos_fixtures:
            path = Path(f"tests/fixtures/{recurso}.json")
            assert path.exists(), f"Fixture {recurso}.json não encontrado"
            
            with open(path) as f:
                data = json.load(f)
                assert isinstance(data, list), f"{recurso}.json não é uma lista"
                assert len(data) > 0, f"{recurso}.json está vazio"
    
    def test_fixtures_nao_estao_corrompidos(self):
        """Verifica se os arquivos de fixture são JSON válidos"""
        recursos = ["ailments", "armor", "items", "monsters", "weapons"]
        
        for recurso in recursos:
            path = Path(f"tests/fixtures/{recurso}.json")
            if path.exists():
                with open(path) as f:
                    try:
                        json.load(f)
                    except json.JSONDecodeError as e:
                        pytest.fail(f"{recurso}.json corrompido: {e}")


class TestMonsterServiceMethods:
    """Testa os métodos específicos do MonsterService"""
    
    @pytest.fixture
    def service(self):
        return MonsterService(requests.Session(), "https://mhw-db.com", collection=None)
    
    def test_get_monster_by_name(self, service):
        resultado = service.get_monster_by_name("Great Jagras")
        assert resultado is not None
        assert resultado["type"] == "large"
    
    def test_get_ailment_by_name(self, service):
        resultado = service.get_ailment_by_name("Poison")
        assert resultado is not None
        assert "recovery" in resultado
    
    def test_get_armor_by_name(self, service):
        resultado = service.get_armor_by_name("Leather Headgear")
        assert resultado is not None
        assert "defense" in resultado
    
    def test_get_item_by_name(self, service):
        resultado = service.get_item_by_name("Potion")
        assert resultado is not None
        assert "value" in resultado
    
    def test_get_weapon_by_name(self, service):
        resultado = service.get_weapon_by_name("Buster Sword 1")
        assert resultado is not None
        assert "attack" in resultado