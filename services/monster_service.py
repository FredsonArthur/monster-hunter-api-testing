# Thuanny Helen - Refatorado para o Hunter Codex (Com Persistência Local)

import json
from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuração do Banco de Dados SQLite
Base = declarative_base()
engine = create_engine('sqlite:///hunter_codex.db')
SessionLocal = sessionmaker(bind=engine)

class MonsterModel(Base):
    __tablename__ = 'monsters'
    name = Column(String, primary_key=True)
    data = Column(JSON)

Base.metadata.create_all(engine)

class MonsterService:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

    def _save_to_db(self, name, data):
        """Salva o resultado da busca no banco de dados local."""
        db = SessionLocal()
        monster = MonsterModel(name=name, data=data)
        db.merge(monster)
        db.commit()
        db.close()

    def get_resource(self, resource_name):
        return self.session.get(f"{self.base_url}/{resource_name}")

    def get_monster_by_name(self, name):
        """Busca um monstro específico: verifica banco local primeiro, depois API."""
        db = SessionLocal()
        cached = db.query(MonsterModel).filter(MonsterModel.name == name).first()
        db.close()

        if cached:
            # Retorna um objeto que simula o response do requests
            class MockResponse:
                def __init__(self, data): self.data = data
                def json(self): return self.data
                @property
                def status_code(self): return 200
            return MockResponse(cached.data)

        # Se não estiver no banco, busca na API e salva
        url = f"{self.base_url}/monsters"
        params = {"q": json.dumps({"name": name})}
        response = self.session.get(url, params=params)
        
        if response.status_code == 200 and response.json():
            self._save_to_db(name, response.json())
            
        return response

    def get_monster_by_id(self, monster_id):
        return self.session.get(f"{self.base_url}/monsters/{monster_id}")

    def get_all_monsters(self):
        return self.session.get(f"{self.base_url}/monsters")