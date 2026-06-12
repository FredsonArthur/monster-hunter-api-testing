import streamlit as st
import pandas as pd
import requests
from services.monster_service import MonsterService

# Inicializa o serviço
service = MonsterService(requests.Session(), "https://mhw-db.com")

st.set_page_config(page_title="Hunter Codex", layout="wide")
st.title("🏹 Hunter Codex Dashboard")

# Busca interativa
nome = st.text_input("Digite o nome do monstro (ex: Great Jagras):")

if nome:
    # Chama o serviço (que agora consulta o MongoDB)
    data = service.get_monster_by_name(nome)
    
    if data:
        st.success(f"Monstro encontrado: {data['name']}")
        
        # Criando o DataFrame para visualização em tabela
        # Filtramos apenas os campos que queremos exibir para a tabela ficar limpa
        display_data = {
            "Nome": [data.get("name")],
            "Tipo": [data.get("type")],
            "Espécie": [data.get("species")],
            "Elemento": [str(data.get("elements"))], # Convertendo lista para string
            "Fraquezas": [str([w['element'] for w in data.get("weaknesses", [])])]
        }
        
        df = pd.DataFrame(display_data)
        
        # Exibe a tabela bonita
        st.table(df)
        
        # Exibe o JSON original caso alguém ainda precise de detalhes técnicos
        with st.expander("Ver dados técnicos brutos (JSON)"):
            st.json(data)
    else:
        st.warning("Monstro não encontrado ou erro na conexão.")