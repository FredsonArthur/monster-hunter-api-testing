# Hunter Codex - Service Layer com MongoDB (Persistência NoSQL)
# ATUALIZADO: Suporte para MÚLTIPLOS recursos (monsters, ailments, armor, items, weapons)

import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from threading import Lock
import requests
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

logger = logging.getLogger(__name__)

class MonsterService:
    # Recursos suportados pela API MHW-DB
    RECURSOS = ["monsters", "ailments", "armor", "items", "weapons"]
    
    # Mapeamento de nomes amigáveis para coleções
    NOME_COLECAO = {
        "monsters": "monsters",
        "ailments": "ailments", 
        "armor": "armor",
        "items": "items",
        "weapons": "weapons"
    }
    
    def __init__(self, session, base_url, mongo_uri='mongodb://localhost:27017/', 
                 collection=None, cache_ttl_hours=168):  # 7 dias padrão
        self.session = session
        self.base_url = base_url
        self.cache_ttl = timedelta(hours=cache_ttl_hours)
        self._locks = {}
        
        # Inicializa conexão com MongoDB
        if collection is not None:
            # Para testes: usa collection mockada
            self.collections = {"default": collection}
            self.mongo_available = True
        else:
            try:
                self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
                self.client.server_info()  # Força conexão
                self.db = self.client['hunter_codex_db']
                self.collections = {}
                # Cria referências para cada coleção
                for recurso in self.RECURSOS:
                    self.collections[recurso] = self.db[self.NOME_COLECAO[recurso]]
                self.mongo_available = True
                logger.info(f"Conectado ao MongoDB com sucesso. Coleções: {list(self.collections.keys())}")
            except ConnectionFailure as e:
                logger.warning(f"Falha ao conectar ao MongoDB: {e}")
                self.collections = {}
                self.mongo_available = False
    
    def _get_collection(self, resource: str):
        """Retorna a coleção correta para o recurso"""
        if not self.mongo_available:
            return None
        return self.collections.get(resource)
    
    def _get_lock(self, key: str):
        """Retorna lock para evitar race conditions"""
        if key not in self._locks:
            self._locks[key] = Lock()
        return self._locks[key]
    
    def _save_to_db(self, resource: str, name: str, data: Dict[str, Any]):
        """Salva ou atualiza o item no MongoDB, na coleção específica do recurso"""
        collection = self._get_collection(resource)
        if collection is None:
            logger.warning(f"MongoDB indisponível, não foi possível cachear {resource}:{name}")
            return
        
        try:
            collection.update_one(
                {"name": name},
                {"$set": {
                    "name": name,
                    "data": data,
                    "resource": resource,
                    "_cached_at": datetime.now(),
                    "_last_updated": datetime.now()
                }},
                upsert=True
            )
            logger.debug(f"Cache atualizado para {resource}:{name}")
        except Exception as e:
            logger.error(f"Erro ao salvar cache para {resource}:{name} - {e}")
    
    def _get_from_cache(self, resource: str, name: str) -> Optional[Dict[str, Any]]:
        """Recupera do MongoDB se existir e não estiver stale"""
        collection = self._get_collection(resource)
        if collection is None:
            return None
        
        try:
            doc = collection.find_one({"name": name})
            if not doc:
                return None
            
            # Verifica idade do cache
            cached_at = doc.get('_cached_at')
            if cached_at:
                if isinstance(cached_at, datetime):
                    age = datetime.now() - cached_at
                    if age > self.cache_ttl:
                        logger.info(f"Cache stale para {resource}:{name} (idade: {age})")
                        return None
            
            logger.debug(f"Cache hit para {resource}:{name}")
            return doc.get('data')
        except Exception as e:
            logger.error(f"Erro ao ler cache para {resource}:{name} - {e}")
            return None
    
    def _fetch_from_api(self, resource: str, name: str) -> Optional[Dict[str, Any]]:
        """Busca item na API e salva no cache"""
        url = f"{self.base_url}/{resource}"
        
        # A API MHW-DB aceita query com nome exato
        params = {"q": json.dumps({"name": name})}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            items = response.json()
            if items and isinstance(items, list) and len(items) > 0:
                # Procura o item com nome exato (case-insensitive)
                found_item = None
                for item in items:
                    if item.get('name', '').lower() == name.lower():
                        found_item = item
                        break
                
                if found_item:
                    self._save_to_db(resource, name, found_item)
                    logger.info(f"{resource.capitalize()} {name} obtido da API e cacheado")
                    return found_item
                else:
                    logger.warning(f"{resource.capitalize()} '{name}' não encontrado na API")
                    return None
            else:
                logger.warning(f"Nenhum {resource} encontrado na API para busca '{name}'")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao buscar {resource}:{name} na API")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"Erro de conexão ao buscar {resource}:{name} na API")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar {resource}:{name} - {e}")
            return None
    
    # ============================================================
    # MÉTODO PRINCIPAL - Busca qualquer recurso por nome
    # ============================================================
    
    def get_by_name(self, resource: str, name: str, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """
        Busca qualquer recurso por nome, com cache MongoDB e fallback para API.
        
        Args:
            resource: Tipo de recurso ('monsters', 'ailments', 'armor', 'items', 'weapons')
            name: Nome do item a buscar
            force_refresh: Se True, ignora cache e busca direto na API
        
        Returns:
            Dicionário com os dados do item, ou None se não encontrado
        """
        if resource not in self.RECURSOS:
            logger.error(f"Recurso inválido: {resource}. Deve ser um de: {self.RECURSOS}")
            return None
        
        lock_key = f"{resource}:{name.lower()}"
        
        with self._get_lock(lock_key):
            if not force_refresh:
                # Tenta cache primeiro
                cached = self._get_from_cache(resource, name)
                if cached:
                    return cached
            
            # Busca na API
            return self._fetch_from_api(resource, name)
    
    # ============================================================
    # MÉTODOS ESPECÍFICOS POR RECURSO (facilidade de uso)
    # ============================================================
    
    def get_monster_by_name(self, name: str, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """Busca monstro por nome"""
        return self.get_by_name("monsters", name, force_refresh)
    
    def get_ailment_by_name(self, name: str, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """Busca status/ailment por nome"""
        return self.get_by_name("ailments", name, force_refresh)
    
    def get_armor_by_name(self, name: str, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """Busca armadura por nome"""
        return self.get_by_name("armor", name, force_refresh)
    
    def get_item_by_name(self, name: str, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """Busca item por nome"""
        return self.get_by_name("items", name, force_refresh)
    
    def get_weapon_by_name(self, name: str, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """Busca arma por nome"""
        return self.get_by_name("weapons", name, force_refresh)
    
    # ============================================================
    # MÉTODOS LEGADOS (mantidos para compatibilidade)
    # ============================================================
    
    def get_resource(self, resource_name: str):
        """Método legado - retorna Response da API sem cache"""
        return self.session.get(f"{self.base_url}/{resource_name}")
    
    def get_monster_by_id(self, monster_id: int):
        """Método legado - busca monstro por ID"""
        return self.session.get(f"{self.base_url}/monsters/{monster_id}")
    
    def get_all_monsters(self):
        """Método legado - retorna todos os monstros"""
        return self.session.get(f"{self.base_url}/monsters")