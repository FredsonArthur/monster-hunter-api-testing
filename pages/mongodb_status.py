"""
Hunter Codex - Status do MongoDB
Exibe informações detalhadas do cache
"""

import sys
import os
import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.monster_service import MonsterService

st.set_page_config(page_title="MongoDB Status", layout="wide")
st.title("🗄️ Status do MongoDB")

# Inicializa serviço
service = MonsterService(requests.Session(), "https://mhw-db.com")

# ============================================================
# STATUS GERAL
# ============================================================
col1, col2, col3 = st.columns(3)

with col1:
    status = "🟢 Conectado" if service.mongo_available else "🔴 Offline"
    st.metric("MongoDB", status)

with col2:
    ttl = service.cache_ttl.days
    st.metric("TTL (dias)", ttl)

with col3:
    if service.mongo_available:
        total = 0
        for recurso in service.RECURSOS:
            colecao = service._get_collection(recurso)
            if colecao is not None:
                try:
                    total += colecao.count_documents({})
                except:
                    pass
        st.metric("Total em cache", total)
    else:
        st.metric("Total em cache", "N/A")

# ============================================================
# DETALHES POR RECURSO
# ============================================================
st.header("📊 Detalhes por Recurso")

if service.mongo_available:
    dados = []
    for recurso in service.RECURSOS:
        colecao = service._get_collection(recurso)
        if colecao is not None:
            try:
                total = colecao.count_documents({})
                # Última atualização
                ultimo = colecao.find_one(sort=[("_last_updated", -1)])
                ultima_atualizacao = ultimo.get("_last_updated") if ultimo else "Nunca"
                
                dados.append({
                    "Recurso": recurso.capitalize(),
                    "Itens": total,
                    "Última atualização": ultima_atualizacao
                })
            except:
                dados.append({
                    "Recurso": recurso.capitalize(),
                    "Itens": "Erro",
                    "Última atualização": "Erro"
                })
    
    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ MongoDB não conectado")

# ============================================================
# TESTE DE CONEXÃO
# ============================================================
st.header("🧪 Teste de Conexão")

if st.button("🔄 Testar conexão com MongoDB"):
    try:
        test_service = MonsterService(requests.Session(), "https://mhw-db.com")
        if test_service.mongo_available:
            st.success("✅ Conexão com MongoDB estabelecida com sucesso!")
            st.json({
                "status": "conectado",
                "ttl": str(test_service.cache_ttl),
                "recursos": test_service.RECURSOS
            })
        else:
            st.error("❌ Falha ao conectar ao MongoDB")
            st.info("Verifique se o MongoDB está rodando:\n```bash\nsudo docker ps | grep mongo\n# ou\nsudo systemctl status mongod\n```")
    except Exception as e:
        st.error(f"❌ Erro: {e}")

# ============================================================
# RODAPÉ
# ============================================================
st.divider()
st.caption(f"🕐 Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")