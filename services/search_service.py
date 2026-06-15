"""
Serviço de busca com autocomplete
Usa os fixtures locais para sugestões rápidas (sem chamar API)
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from difflib import get_close_matches

class SearchService:
    """Serviço para busca parcial e autocomplete usando fixtures locais"""
    
    def __init__(self):
        self.cache_busca = {}  # Cache em memória para buscas
        self._carregar_fixtures()
    
    def _carregar_fixtures(self):
        """Carrega todos os nomes dos fixtures para busca rápida"""
        recursos = ["monsters", "ailments", "armor", "items", "weapons"]
        
        for recurso in recursos:
            # Tenta diferentes caminhos possíveis
            caminhos_tentativa = [
                Path(f"tests/fixtures/{recurso}.json"),
                Path(f"../tests/fixtures/{recurso}.json"),
                Path(f"../../tests/fixtures/{recurso}.json"),
                Path(__file__).parent.parent / f"tests/fixtures/{recurso}.json"
            ]
            
            caminho_encontrado = None
            for caminho in caminhos_tentativa:
                if caminho.exists():
                    caminho_encontrado = caminho
                    break
            
            if caminho_encontrado:
                try:
                    with open(caminho_encontrado) as f:
                        dados = json.load(f)
                        # Extrai nomes de cada item
                        self.cache_busca[recurso] = [
                            {"name": item.get("name"), "id": item.get("id")}
                            for item in dados
                            if item.get("name")
                        ]
                except Exception as e:
                    print(f"Erro ao carregar {recurso}: {e}")
                    self.cache_busca[recurso] = []
            else:
                print(f"Arquivo não encontrado: tests/fixtures/{recurso}.json")
                self.cache_busca[recurso] = []
    
    def autocomplete(self, recurso: str, termo: str, limite: int = 5) -> List[Dict[str, Any]]:
        """
        Retorna sugestões baseadas no termo digitado
        
        Args:
            recurso: Tipo de recurso (monsters, ailments, etc.)
            termo: O que o usuário digitou
            limite: Número máximo de sugestões
        
        Returns:
            Lista de sugestões com nome e id
        """
        if not termo or len(termo) < 2:
            return []
        
        termo_lower = termo.lower()
        sugestoes = []
        
        for item in self.cache_busca.get(recurso, []):
            nome = item.get("name", "")
            nome_lower = nome.lower()
            
            # Busca por início da palavra (ex: "Jag" → "Great Jagras")
            if nome_lower.startswith(termo_lower):
                sugestoes.append(item)
            
            # Busca por palavra contida (ex: "Jag" → "Great Jagras" também)
            elif termo_lower in nome_lower:
                sugestoes.append(item)
            
            if len(sugestoes) >= limite:
                break
        
        # Se poucas sugestões, tenta fuzzy matching
        if len(sugestoes) < 3:
            nomes = [item.get("name") for item in self.cache_busca.get(recurso, [])]
            matches = get_close_matches(termo, nomes, n=limite, cutoff=0.6)
            
            for match in matches:
                # Evita duplicatas
                if not any(s.get("name") == match for s in sugestoes):
                    # Encontra o item completo
                    for item in self.cache_busca.get(recurso, []):
                        if item.get("name") == match:
                            sugestoes.append(item)
                            break
        
        return sugestoes[:limite]
    
    def get_all_names(self, recurso: str) -> List[str]:
        """Retorna todos os nomes de um recurso"""
        return [item.get("name") for item in self.cache_busca.get(recurso, []) if item.get("name")]