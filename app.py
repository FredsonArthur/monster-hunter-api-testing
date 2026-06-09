import streamlit as st
from services.monster_service import MonsterService
import requests

# Inicializa o serviço
service = MonsterService(requests.Session(), "https://mhw-db.com")

st.title("🏹 Hunter Codex Dashboard")
st.write("Bem-vindo ao buscador de monstros oficial.")

# Busca interativa
nome = st.text_input("Digite o nome do monstro (ex: Great Jagras):")

if nome:
    response = service.get_monster_by_name(nome)
    if response.status_code == 200:
        data = response.json()
        if data:
            st.success(f"Monstro encontrado: {data[0]['name']}")
            st.json(data[0])
        else:
            st.warning("Monstro não encontrado.")
    else:
        st.error("Erro ao buscar na API.")