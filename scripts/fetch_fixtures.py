import requests
import json
import os

RECURSOS = ["ailments", "armor", "items", "monsters", "weapons"]
BASE_URL = "https://mhw-db.com"

def fetch_and_save():
    if not os.path.exists('tests/fixtures'):
        os.makedirs('tests/fixtures')

    for recurso in RECURSOS:
        print(f"Coletando {recurso}...")
        response = requests.get(f"{BASE_URL}/{recurso}")
        
        if response.status_code == 200:
            with open(f"tests/fixtures/{recurso}.json", "w") as f:
                json.dump(response.json(), f, indent=4)
            print(f"Sucesso: {recurso}.json criado!")
        else:
            print(f"Erro ao coletar {recurso}: {response.status_code}")

if __name__ == "__main__":
    fetch_and_save()