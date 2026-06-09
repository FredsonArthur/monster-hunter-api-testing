# Thuanny Helen - Refatorado para o Hunter Codex

import json

class MonsterService:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

    def get_resource(self, resource_name):
        """Método genérico para buscar qualquer recurso (ailments, armor, items, etc)."""
        return self.session.get(f"{self.base_url}/{resource_name}")

    def get_monster_by_name(self, name):
        """Busca um monstro específico pelo nome."""
        url = f"{self.base_url}/monsters"
        params = {"q": json.dumps({"name": name})}
        return self.session.get(url, params=params)

    def get_monster_by_id(self, monster_id):
        """Busca um monstro específico pelo ID."""
        return self.session.get(f"{self.base_url}/monsters/{monster_id}")

    def get_all_monsters(self):
        """Retorna todos os monstros."""
        return self.session.get(f"{self.base_url}/monsters")