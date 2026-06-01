#Thuanny Helen

import json

class MonsterService:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = f"{base_url}/monsters"

    def get_monster_by_name(self, name):
        """Busca um monstro específico pelo nome."""
        params = {"q": json.dumps({"name": name})}
        return self.session.get(self.base_url, params=params)

    def get_monster_by_id(self, monster_id):
        """Busca um monstro específico pelo ID."""
        return self.session.get(f"{self.base_url}/{monster_id}")

    def get_all_monsters(self):
        """Retorna todos os monstros."""
        return self.session.get(self.base_url)