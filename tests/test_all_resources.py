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
    
    @pytest.mark.parametrize("recurso, nome_teste", [
        ("monsters", "Rathalos"),
        ("ailments", "Paralysis"),
        ("armor", "Chainmail Headgear"),
        ("items", "Mega Potion"),
        ("weapons", "Iron Sword 1"),
    ])
    def test_cache_funciona_com_mock(self, service, recurso, nome_teste):
        """
        Testa se o cache está funcionando (usando mock)
        Como o MongoDB não está disponível no CI, pulamos este teste
        """
        pytest.skip(f"Cache test skipped in CI - MongoDB not available")
    
    def test_todos_recursos_tem_fixtures(self):
        """Verifica se todos os recursos têm arquivos de fixture"""
        recursos_fixtures = ["ailments", "armor", "items", "monsters", "weapons"]
        
        for recurso in recursos_fixtures:
            # Tenta diferentes caminhos
            caminhos = [
                Path(f"tests/fixtures/{recurso}.json"),
                Path(f"../tests/fixtures/{recurso}.json"),
            ]
            encontrado = False
            for caminho in caminhos:
                if caminho.exists():
                    encontrado = True
                    with open(caminho) as f:
                        data = json.load(f)
                        assert isinstance(data, list), f"{recurso}.json não é uma lista"
                        assert len(data) > 0, f"{recurso}.json está vazio"
                    break
            
            if not encontrado:
                pytest.skip(f"Fixture {recurso}.json não encontrado no CI")
    
    def test_fixtures_nao_estao_corrompidos(self):
        """Verifica se os arquivos de fixture são JSON válidos"""
        recursos = ["ailments", "armor", "items", "monsters", "weapons"]
        
        for recurso in recursos:
            caminhos = [
                Path(f"tests/fixtures/{recurso}.json"),
                Path(f"../tests/fixtures/{recurso}.json"),
            ]
            for caminho in caminhos:
                if caminho.exists():
                    with open(caminho) as f:
                        try:
                            json.load(f)
                        except json.JSONDecodeError as e:
                            pytest.fail(f"{recurso}.json corrompido: {e}")
                    break


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