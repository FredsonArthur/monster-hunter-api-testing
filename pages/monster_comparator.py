"""
Hunter Codex - Comparador de Monstros
Permite comparar dois monstros lado a lado
"""

import sys
import os
import streamlit as st
import pandas as pd
import requests

# Adiciona o diretório raiz ao path para importar os serviços
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.monster_service import MonsterService
from services.search_service import SearchService

st.set_page_config(page_title="Comparador de Monstros", layout="wide")
st.title("🐉 Comparador de Monstros")

# Inicializa serviços
service = MonsterService(requests.Session(), "https://mhw-db.com")
search_service = SearchService()

# ============================================================
# SIDEBAR - Configurações
# ============================================================
with st.sidebar:
    st.header("⚙️ Configurações")
    force_refresh = st.checkbox("🔄 Ignorar cache (buscar da API)", value=False)
    st.divider()
    st.caption(f"MongoDB: {'Conectado' if service.mongo_available else 'Offline (usando só API)'}")

# ============================================================
# ÁREA PRINCIPAL - Seleção dos Monstros
# ============================================================
st.markdown("Compare dois monstros lado a lado para ver diferenças de fraquezas, resistências e mais!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🥇 Monstro 1")
    nome1 = st.text_input(
        "Digite o nome do primeiro monstro:",
        placeholder="Ex: Great Jagras",
        key="monster1_input"
    )
    
    # Autocomplete para monstro 1
    if nome1 and len(nome1) >= 2:
        sugestoes = search_service.autocomplete("monsters", nome1, limite=5)
        if sugestoes:
            opcoes = [f"{s['name']}" for s in sugestoes]
            selecionado = st.selectbox(
                "Sugestões:",
                options=[""] + opcoes,
                key="auto1",
                label_visibility="collapsed"
            )
            if selecionado:
                nome1 = selecionado

with col2:
    st.subheader("🥈 Monstro 2")
    nome2 = st.text_input(
        "Digite o nome do segundo monstro:",
        placeholder="Ex: Rathalos",
        key="monster2_input"
    )
    
    # Autocomplete para monstro 2
    if nome2 and len(nome2) >= 2:
        sugestoes = search_service.autocomplete("monsters", nome2, limite=5)
        if sugestoes:
            opcoes = [f"{s['name']}" for s in sugestoes]
            selecionado = st.selectbox(
                "Sugestões:",
                options=[""] + opcoes,
                key="auto2",
                label_visibility="collapsed"
            )
            if selecionado:
                nome2 = selecionado

# Botão de comparação
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    comparar = st.button("🔍 COMPARAR", type="primary", use_container_width=True)

# ============================================================
# RESULTADOS DA COMPARAÇÃO
# ============================================================
if comparar and nome1 and nome2:
    with st.spinner("Buscando dados dos monstros..."):
        monstro1 = service.get_by_name("monsters", nome1, force_refresh=force_refresh)
        monstro2 = service.get_by_name("monsters", nome2, force_refresh=force_refresh)
    
    if monstro1 is None:
        st.error(f"❌ Monstro '{nome1}' não encontrado!")
    
    if monstro2 is None:
        st.error(f"❌ Monstro '{nome2}' não encontrado!")
    
    if monstro1 and monstro2:
        st.success(f"✅ Comparando **{monstro1.get('name')}** vs **{monstro2.get('name')}**")
        
        # ====================================================
        # TABELA DE COMPARAÇÃO
        # ====================================================
        
        # Informações Básicas
        st.header("📊 Informações Básicas")
        info_data = {
            "Atributo": ["Tipo", "Espécie", "Elementos"],
            monstro1.get('name', 'Monstro 1'): [
                monstro1.get('type', 'N/A'),
                monstro1.get('species', 'N/A'),
                ', '.join(monstro1.get('elements', [])) or 'Nenhum'
            ],
            monstro2.get('name', 'Monstro 2'): [
                monstro2.get('type', 'N/A'),
                monstro2.get('species', 'N/A'),
                ', '.join(monstro2.get('elements', [])) or 'Nenhum'
            ]
        }
        df_info = pd.DataFrame(info_data)
        st.dataframe(df_info, use_container_width=True, hide_index=True)
        
        # Fraquezas lado a lado
        st.header("🎯 Fraquezas")
        
        # Extrai fraquezas
        weak1 = {w.get('element', '').lower(): w.get('stars', 0) for w in monstro1.get('weaknesses', [])}
        weak2 = {w.get('element', '').lower(): w.get('stars', 0) for w in monstro2.get('weaknesses', [])}
        
        todos_elementos = sorted(set(list(weak1.keys()) + list(weak2.keys())))
        
        fraquezas_data = {
            "Elemento": [],
            monstro1.get('name', 'M1'): [],
            monstro2.get('name', 'M2'): []
        }
        
        for elemento in todos_elementos:
            fraquezas_data["Elemento"].append(elemento.capitalize())
            fraquezas_data[monstro1.get('name', 'M1')].append("★" * weak1.get(elemento, 0) or "☆")
            fraquezas_data[monstro2.get('name', 'M2')].append("★" * weak2.get(elemento, 0) or "☆")
        
        df_weak = pd.DataFrame(fraquezas_data)
        st.dataframe(df_weak, use_container_width=True, hide_index=True)
        
        # Resistências
        st.header("🛡️ Resistências")
        
        res1 = {r.get('element', '').lower(): r.get('condition', '') for r in monstro1.get('resistances', [])}
        res2 = {r.get('element', '').lower(): r.get('condition', '') for r in monstro2.get('resistances', [])}
        
        todos_res = sorted(set(list(res1.keys()) + list(res2.keys())))
        
        resist_data = {
            "Elemento": [],
            monstro1.get('name', 'M1'): [],
            monstro2.get('name', 'M2'): []
        }
        
        for elemento in todos_res:
            resist_data["Elemento"].append(elemento.capitalize())
            resist_data[monstro1.get('name', 'M1')] = res1.get(elemento, 'Nenhuma') or 'Imune'
            resist_data[monstro2.get('name', 'M2')] = res2.get(elemento, 'Nenhuma') or 'Imune'
        
        df_res = pd.DataFrame(resist_data)
        st.dataframe(df_res, use_container_width=True, hide_index=True)
        
        # Locais
        st.header("📍 Locais Onde Aparecem")
        
        loc1 = [loc.get('name', 'Unknown') for loc in monstro1.get('locations', [])]
        loc2 = [loc.get('name', 'Unknown') for loc in monstro2.get('locations', [])]
        
        locais_data = {
            monstro1.get('name', 'Monstro 1'): ", ".join(loc1) or "Nenhum",
            monstro2.get('name', 'Monstro 2'): ", ".join(loc2) or "Nenhum"
        }
        
        for monstro, locais in locais_data.items():
            st.write(f"**{monstro}:** {locais}")
        
        # ====================================================
        # GRÁFICO DE COMPARAÇÃO DE FRAQUEZAS
        # ====================================================
        st.header("📊 Comparação Visual de Fraquezas")
        
        # Prepara dados para o gráfico
        import plotly.express as px
        
        grafico_data = []
        for elemento in todos_elementos:
            grafico_data.append({
                "Elemento": elemento.capitalize(),
                "Monstro": monstro1.get('name', 'M1'),
                "Estrelas": weak1.get(elemento, 0)
            })
            grafico_data.append({
                "Elemento": elemento.capitalize(),
                "Monstro": monstro2.get('name', 'M2'),
                "Estrelas": weak2.get(elemento, 0)
            })
        
        if grafico_data:
            df_grafico = pd.DataFrame(grafico_data)
            fig = px.bar(
                df_grafico,
                x="Elemento",
                y="Estrelas",
                color="Monstro",
                barmode="group",
                title="Comparação de Fraquezas por Elemento",
                labels={"Estrelas": "Nível de Fraqueza (★)", "Elemento": "Elemento"},
                color_discrete_sequence=["#ff6b6b", "#4ecdc4"]
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Dados brutos (opcional)
        with st.expander("📄 Ver dados técnicos completos (JSON)"):
            col_json1, col_json2 = st.columns(2)
            with col_json1:
                st.subheader(monstro1.get('name'))
                st.json(monstro1)
            with col_json2:
                st.subheader(monstro2.get('name'))
                st.json(monstro2)

elif comparar:
    st.warning("⚠️ Por favor, digite o nome de dois monstros para comparar.")

# ============================================================
# RODAPÉ
# ============================================================
st.divider()
st.caption("🐉 Hunter Codex - Compare as fraquezas e características dos monstros!")