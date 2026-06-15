"""
Hunter Codex - Dashboard de Saúde
Mostra status do MongoDB, cache e performance do sistema
"""

import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
from services.monster_service import MonsterService

st.set_page_config(page_title="Health Dashboard", layout="wide")
st.title("🏥 Hunter Codex - Dashboard de Saúde")

# Inicializa serviço
service = MonsterService(requests.Session(), "https://mhw-db.com")

# ============================================================
# CARDS DE STATUS
# ============================================================
st.header("📊 Status do Sistema")

col1, col2, col3, col4 = st.columns(4)

with col1:
    mongo_status = "🟢 Conectado" if service.mongo_available else "🔴 Offline"
    st.metric("MongoDB", mongo_status)

with col2:
    recursos = len(service.RECURSOS)
    st.metric("Recursos Suportados", recursos)

with col3:
    try:
        response = requests.get("https://mhw-db.com", timeout=5)
        api_status = "🟢 Online" if response.status_code == 200 else "🟡 Instável"
    except:
        api_status = "🔴 Offline"
    st.metric("API MHW-DB", api_status)

with col4:
    st.metric("Cache TTL", f"{service.cache_ttl.days} dias")

# ============================================================
# TESTE RÁPIDO DE CADA RECURSO
# ============================================================
st.header("🧪 Teste Rápido de Recursos")

testes = [
    ("🐉 Monstros", "monsters", "Great Jagras"),
    ("💀 Ailments", "ailments", "Poison"),
    ("🛡️ Armaduras", "armor", "Leather Headgear"),
    ("📦 Itens", "items", "Potion"),
    ("⚔️ Armas", "weapons", "Buster Sword 1"),
]

resultados = []
for nome_recurso, recurso, exemplo in testes:
    start = time.time()
    resultado = service.get_by_name(recurso, exemplo)
    end = time.time()
    
    tempo = (end - start) * 1000  # em ms
    
    resultados.append({
        "Recurso": nome_recurso,
        "Exemplo": exemplo,
        "Encontrado": "✅ Sim" if resultado else "❌ Não",
        "Tempo (ms)": f"{tempo:.0f}",
        "Cache usado": "✅" if resultado and "_cached_at" in str(resultado) else "❌"
    })

df_resultados = pd.DataFrame(resultados)
st.dataframe(df_resultados, use_container_width=True)

# ============================================================
# ESTATÍSTICAS DE CACHE (se MongoDB conectado)
# ============================================================
if service.mongo_available:
    st.header("💾 Estatísticas do Cache")
    
    cache_stats = []
    for recurso in service.RECURSOS:
        try:
            colecao = service._get_collection(recurso)
            if colecao:
                total = colecao.count_documents({})
                
                # Itens cacheados na última hora
                uma_hora_atras = datetime.now().timestamp() - 3600
                recentes = colecao.count_documents({
                    "_last_updated": {"$gt": uma_hora_atras}
                })
                
                cache_stats.append({
                    "Recurso": recurso.capitalize(),
                    "Itens em Cache": total,
                    "Atualizados (última hora)": recentes
                })
        except Exception as e:
            cache_stats.append({
                "Recurso": recurso.capitalize(),
                "Itens em Cache": "Erro",
                "Atualizados (última hora)": str(e)
            })
    
    if cache_stats:
        df_cache = pd.DataFrame(cache_stats)
        st.dataframe(df_cache, use_container_width=True)
else:
    st.warning("🔴 MongoDB não conectado. Estatísticas de cache indisponíveis.")
    st.info("Para conectar, execute `mongod` em outro terminal e reinicie o app.")

# ============================================================
# PERFORMANCE
# ============================================================
st.header("⚡ Performance")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Teste de Latência - API")
    with st.spinner("Testando..."):
        try:
            start = time.time()
            response = requests.get("https://mhw-db.com/monsters", timeout=10)
            end = time.time()
            api_latency = (end - start) * 1000
            st.success(f"✅ {api_latency:.0f} ms")
        except Exception as e:
            st.error(f"❌ Erro: {e}")

with col2:
    st.subheader("Teste de Cache - MongoDB")
    with st.spinner("Testando..."):
        start = time.time()
        resultado = service.get_by_name("monsters", "Rathalos")
        end = time.time()
        cache_latency = (end - start) * 1000
        if resultado:
            st.success(f"✅ {cache_latency:.0f} ms")
        else:
            st.warning("Cache vazio (primeira busca pode ser mais lenta)")

# ============================================================
# CONFIGURAÇÕES ATUAIS
# ============================================================
st.header("⚙️ Configurações")

config_data = {
    "Configuração": [
        "URL da API",
        "Cache TTL",
        "MongoDB URI",
        "Recursos",
        "Timeout da API"
    ],
    "Valor": [
        service.base_url,
        f"{service.cache_ttl.days} dias",
        "mongodb://localhost:27017/",
        ", ".join(service.RECURSOS),
        "10 segundos"
    ]
}

df_config = pd.DataFrame(config_data)
st.dataframe(df_config, use_container_width=True, hide_index=True)

# ============================================================
# RODAPÉ
# ============================================================
st.divider()
st.caption(f"🕐 Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")