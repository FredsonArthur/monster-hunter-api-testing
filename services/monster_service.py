# Hunter Codex - Service Layer com MongoDB (Persistência NoSQL)

import json
from pymongo import MongoClient

class MonsterService:
    def __init__(self, session, base_url, mongo_uri='mongodb://localhost:27017/'):
        self.session = session
        self.base_url = base_url
        # Conexão com MongoDB
        self.client = MongoClient(mongo_uri)
        self.db = self.client['hunter_codex_db']
        self.collection = self.db['monsters']

    def _save_to_db(self, name, data):
        """Salva ou atualiza o monstro no MongoDB."""
        # Usamos update_one com upsert=True para não duplicar registros
        self.collection.update_one(
            {"name": name}, 
            {"$set": {"name": name, "data": data}}, 
            upsert=True
        )

    def get_resource(self, resource_name):
        return self.session.get(f"{self.base_url}/{resource_name}")

    def get_monster_by_name(self, name):
        """Busca no MongoDB local primeiro; se não encontrar, busca na API."""
        cached = self.collection.find_one({"name": name})
        
        if cached:
            # Classe auxiliar para simular o comportamento de um Response do requests
            class MockResponse:
                def __init__(self, data): self.data = data
                def json(self): return self.data
                @property
                def status_code(self): return 200
            return MockResponse(cached['data'])

        # Busca na API
        url = f"{self.base_url}/monsters"
        params = {"q": json.dumps({"name": name})}
        response = self.session.get(url, params=params)
        
        if response.status_code == 200 and response.json():
            # A API retorna uma lista, salvamos o conteúdo
            data = response.json()
            self._save_to_db(name, data)
            
        return response

    def get_monster_by_id(self, monster_id):
        return self.session.get(f"{self.base_url}/monsters/{monster_id}")

    def get_all_monsters(self):
        return self.session.get(f"{self.base_url}/monsters")