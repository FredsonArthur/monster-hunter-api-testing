import streamlit as st
import pandas as pd
import requests
from services.monster_service import MonsterService
from services.search_service import SearchService

# ============================================================
# INICIALIZAÇÃO DO MONGODB
# ============================================================
if 'mongodb_ativado' not in st.session_state:
    st.session_state.mongodb_ativado = True

if 'ttl_hours' not in st.session_state:
    st.session_state.ttl_hours = 168

if 'ultima_atualizacao' not in st.session_state:
    st.session_state.ultima_atualizacao = None

# ============================================================
# INICIALIZAÇÃO DO HISTÓRICO
# ============================================================
if 'historico' not in st.session_state:
    st.session_state.historico = []

def adicionar_ao_historico(termo, recurso):
    item = {"termo": termo, "recurso": recurso}
    st.session_state.historico = [i for i in st.session_state.historico if i["termo"] != termo or i["recurso"] != recurso]
    st.session_state.historico.insert(0, item)
    st.session_state.historico = st.session_state.historico[:10]

# ============================================================
# INICIALIZAÇÃO DOS FAVORITOS
# ============================================================
if 'favoritos' not in st.session_state:
    st.session_state.favoritos = []

def adicionar_favorito(termo, recurso):
    item = {"termo": termo, "recurso": recurso}
    if item not in st.session_state.favoritos:
        st.session_state.favoritos.append(item)
        return True
    return False

def remover_favorito(termo, recurso):
    item = {"termo": termo, "recurso": recurso}
    if item in st.session_state.favoritos:
        st.session_state.favoritos.remove(item)
        return True
    return False

def is_favorito(termo, recurso):
    for fav in st.session_state.favoritos:
        if fav["termo"] == termo and fav["recurso"] == recurso:
            return True
    return False

# ============================================================
# INICIALIZAÇÃO DO SERVIÇO
# ============================================================
@st.cache_resource
def get_service(ttl_hours):
    return MonsterService(
        requests.Session(),
        "https://mhw-db.com",
        cache_ttl_hours=ttl_hours
    )

service = get_service(st.session_state.ttl_hours)
search_service = SearchService()

def reiniciar_servico_com_ttl(ttl_horas):
    st.cache_resource.clear()
    st.session_state.ttl_hours = ttl_horas
    st.session_state.ultima_atualizacao = None
    st.rerun()

st.set_page_config(page_title="Hunter Codex", layout="wide")
st.title("🏹 Hunter Codex Dashboard")

# ============================================================
# SIDEBAR - Configurações
# ============================================================
with st.sidebar:
    st.header("⚙️ Configurações")
    
    recurso_opcoes = {
        "🐉 Monstros": "monsters",
        "💀 Ailments (Status)": "ailments",
        "🛡️ Armaduras": "armor",
        "📦 Itens": "items",
        "⚔️ Armas": "weapons"
    }
    
    recurso_selecionado = st.selectbox(
        "📋 Tipo de busca:",
        list(recurso_opcoes.keys())
    )
    
    recurso = recurso_opcoes[recurso_selecionado]
    
    st.divider()
    
    # ========================================================
    # CONFIGURAÇÕES DO MONGODB
    # ========================================================
    st.subheader("🗄️ MongoDB")
    
    mongodb_ativado = st.checkbox(
        "✅ Ativar cache MongoDB",
        value=st.session_state.mongodb_ativado,
        help="Quando ativado, os dados são salvos no MongoDB. Quando desativado, busca direto da API."
    )
    
    if mongodb_ativado != st.session_state.mongodb_ativado:
        st.session_state.mongodb_ativado = mongodb_ativado
        st.rerun()
    
    if st.session_state.mongodb_ativado:
        ttl_horas = st.slider(
            "⏰ Tempo de atualização (horas)",
            min_value=1,
            max_value=720,
            value=st.session_state.ttl_hours,
            step=1,
            help="Tempo que o cache fica válido. Após isso, os dados são atualizados da API."
        )
        
        if ttl_horas != st.session_state.ttl_hours:
            reiniciar_servico_com_ttl(ttl_horas)
        
        st.caption(f"🕐 TTL atual: {st.session_state.ttl_hours} horas ({st.session_state.ttl_hours/24:.1f} dias)")
        
        if st.button("🧹 Limpar cache", type="secondary"):
            if service.mongo_available:
                total_removidos = 0
                for recurso_tipo in service.RECURSOS:
                    colecao = service._get_collection(recurso_tipo)
                    if colecao is not None:
                        try:
                            resultado = colecao.delete_many({})
                            total_removidos += resultado.deleted_count
                        except:
                            pass
                st.info(f"🗑️ Removidos {total_removidos} itens do cache")
                st.session_state.ultima_atualizacao = None
                st.rerun()
            else:
                st.warning("⚠️ MongoDB não disponível para limpar cache")
    
    st.divider()
    
    # ========================================================
    # ESTATÍSTICAS DO CACHE
    # ========================================================
    if st.session_state.mongodb_ativado and service.mongo_available:
        st.subheader("📊 Estatísticas do Cache")
        
        total_itens = 0
        for recurso_tipo in service.RECURSOS:
            colecao = service._get_collection(recurso_tipo)
            if colecao is not None:
                try:
                    count = colecao.count_documents({})
                    total_itens += count
                    st.caption(f"**{recurso_tipo.capitalize()}:** {count} itens")
                except:
                    pass
        
        st.caption(f"**Total:** {total_itens} itens cacheados")
        
        if st.session_state.ultima_atualizacao:
            st.caption(f"🔄 Última atualização: {st.session_state.ultima_atualizacao}")
    
    # ========================================================
    # FAVORITOS
    # ========================================================
    st.divider()
    st.subheader("⭐ Favoritos")
    
    if st.session_state.favoritos:
        st.caption(f"{len(st.session_state.favoritos)} item(ns) favoritado(s)")
        
        for i, fav in enumerate(st.session_state.favoritos):
            cols = st.columns([4, 1])
            with cols[0]:
                if st.button(f"🔍 {fav['termo']}", key=f"fav_btn_{i}"):
                    nome = fav['termo']
                    recurso_selecionado = list(recurso_opcoes.keys())[list(recurso_opcoes.values()).index(fav['recurso'])]
                    buscar = True
            with cols[1]:
                if st.button("🗑️", key=f"fav_del_{i}"):
                    remover_favorito(fav['termo'], fav['recurso'])
                    st.rerun()
    else:
        st.caption("Nenhum favorito ainda. Use ⭐ nos resultados!")
    
    st.divider()
    force_refresh = st.checkbox(
        "🔄 Ignorar cache (buscar da API)",
        value=False,
        help="Força a busca diretamente da API, ignorando o cache"
    )
    
    st.divider()
    st.caption(f"MongoDB: {'🟢 Conectado' if service.mongo_available else '🔴 Offline'}")

# ============================================================
# ÁREA PRINCIPAL - Busca
# ============================================================
col1, col2 = st.columns([3, 1])

with col1:
    nome = st.text_input(
        f"🔍 Digite o nome do {recurso_selecionado.lower()}:",
        placeholder="Ex: Great Jagras, Potion, Leather Headgear...",
        help="Digite termos familiares ou parte do nome. Use sugestões para selecionar rapidamente o item correto.",
        key="search_input"
    )
    
    if nome and len(nome) >= 2:
        sugestoes = search_service.autocomplete(recurso, nome, limite=5)
        if sugestoes:
            opcoes = [f"{s['name']}" for s in sugestoes]
            selecionado = st.selectbox(
                "💡 Sugestões:",
                options=[""] + opcoes,
                key="autocomplete",
                label_visibility="collapsed"
            )
            if selecionado:
                nome = selecionado

with col2:
    st.write("")
    st.write("")
    buscar = st.button("🔍 Buscar", type="primary", use_container_width=True)

# ============================================================
# HISTÓRICO DE BUSCAS
# ============================================================
if st.session_state.historico:
    with st.expander("📜 Histórico de buscas (últimas 10)"):
        for i, item in enumerate(st.session_state.historico):
            cols = st.columns([6, 1, 1])
            with cols[0]:
                if st.button(f"🔍 {item['termo']} ({item['recurso']})", key=f"hist_{i}"):
                    nome = item['termo']
                    recurso_selecionado = list(recurso_opcoes.keys())[list(recurso_opcoes.values()).index(item['recurso'])]
                    buscar = True
            with cols[1]:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.historico.pop(i)
                    st.rerun()
            with cols[2]:
                if is_favorito(item['termo'], item['recurso']):
                    if st.button("⭐", key=f"fav_hist_{i}"):
                        remover_favorito(item['termo'], item['recurso'])
                        st.rerun()
                else:
                    if st.button("☆", key=f"fav_hist_{i}"):
                        adicionar_favorito(item['termo'], item['recurso'])
                        st.toast(f"⭐ Adicionado aos favoritos: {item['termo']}", icon="⭐")
                        st.rerun()

# ============================================================
# Busca Rápida por Letra
# ============================================================
with st.expander("🔤 Busca rápida por letra"):
    st.caption("Clique em uma letra para buscar o primeiro item que começa com ela")
    letras = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    cols = st.columns(13)
    for i, letra in enumerate(letras):
        with cols[i % 13]:
            if st.button(letra, key=f"letra_{letra}"):
                todos_nomes = search_service.get_all_names(recurso)
                for nome_item in todos_nomes:
                    if nome_item and nome_item.upper().startswith(letra):
                        nome = nome_item
                        buscar = True
                        break

# ============================================================
# RESULTADOS
# ============================================================
if buscar and nome:
    adicionar_ao_historico(nome, recurso)
    
    from datetime import datetime
    st.session_state.ultima_atualizacao = datetime.now().strftime("%H:%M:%S")
    
    with st.spinner(f"Buscando {nome} em {recurso_selecionado}..."):
        data = service.get_by_name(recurso, nome, force_refresh=force_refresh)
    
    if data:
        col_titulo, col_botoes = st.columns([4, 1])
        
        with col_titulo:
            st.success(f"✅ {recurso_selecionado} encontrado: **{data.get('name')}**")
        
        with col_botoes:
            item_nome = data.get('name')
            if is_favorito(item_nome, recurso):
                if st.button("⭐ Favorito", key=f"fav_remover_{item_nome}", type="primary"):
                    remover_favorito(item_nome, recurso)
                    st.toast(f"❌ Removido dos favoritos: {item_nome}", icon="⭐")
            else:
                if st.button("☆ Adicionar", key=f"fav_adicionar_{item_nome}"):
                    adicionar_favorito(item_nome, recurso)
                    st.toast(f"⭐ Adicionado aos favoritos: {item_nome}", icon="⭐")
        
        # ====================================================
        # EXIBIÇÃO ESPECÍFICA POR TIPO DE RECURSO
        # ====================================================
        
        if recurso == "monsters":
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("📊 Informações Básicas")
                st.write(f"**Tipo:** {data.get('type', 'N/A')}")
                st.write(f"**Espécie:** {data.get('species', 'N/A')}")
                st.write(f"**Elementos:** {', '.join(data.get('elements', [])) if data.get('elements') else 'Nenhum'}")
            
            with col2:
                st.subheader("🎯 Fraquezas")
                weaknesses = data.get('weaknesses', [])
                if weaknesses:
                    for w in weaknesses:
                        stars = "★" * w.get('stars', 0)
                        st.write(f"**{w.get('element', 'Unknown').capitalize()}:** {stars}")
                else:
                    st.write("Nenhuma fraqueza listada")
            
            st.subheader("🛡️ Resistências")
            resistances = data.get('resistances', [])
            if resistances:
                for r in resistances:
                    cond = f" ({r.get('condition')})" if r.get('condition') else ""
                    st.write(f"**{r.get('element', 'Unknown').capitalize()}**{cond}")
            else:
                st.write("Nenhuma resistência listada")
            
            st.subheader("📍 Locais")
            locations = data.get('locations', [])
            if locations:
                for loc in locations:
                    st.write(f"- {loc.get('name', 'Unknown')}")
            else:
                st.write("Nenhum local listado")
        
        elif recurso == "ailments":
            st.subheader("📝 Descrição")
            st.write(data.get('description', 'Sem descrição'))
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💊 Como Curar")
                recovery = data.get('recovery', {})
                acoes = recovery.get('actions', [])
                itens = recovery.get('items', [])
                
                if acoes:
                    st.write("**Ações:**")
                    for acao in acoes:
                        st.write(f"- {acao}")
                
                if itens:
                    st.write("**Itens:**")
                    for item in itens:
                        st.write(f"- {item.get('name', 'Unknown')}")
                
                if not acoes and not itens:
                    st.write("Nenhum método de cura listado")
            
            with col2:
                st.subheader("🛡️ Como Prevenir")
                protection = data.get('protection', {})
                skills = protection.get('skills', [])
                itens_prot = protection.get('items', [])
                
                if skills:
                    st.write("**Habilidades:**")
                    for skill in skills:
                        st.write(f"- {skill.get('name', 'Unknown')}")
                
                if itens_prot:
                    st.write("**Itens:**")
                    for item in itens_prot:
                        st.write(f"- {item.get('name', 'Unknown')}")
                
                if not skills and not itens_prot:
                    st.write("Nenhum método de prevenção listado")
        
        elif recurso == "armor":
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🛡️ Defesa")
                defense = data.get('defense', {})
                st.write(f"**Base:** {defense.get('base', 'N/A')}")
                st.write(f"**Máxima:** {defense.get('max', 'N/A')}")
                
                st.subheader("⭐ Raridade")
                st.write(f"{data.get('rarity', 'N/A')}")
            
            with col2:
                st.subheader("🔥 Resistências")
                resist = data.get('resistances', {})
                st.write(f"**Fogo:** {resist.get('fire', 0)}")
                st.write(f"**Água:** {resist.get('water', 0)}")
                st.write(f"**Gelo:** {resist.get('ice', 0)}")
                st.write(f"**Raio:** {resist.get('thunder', 0)}")
                st.write(f"**Dragão:** {resist.get('dragon', 0)}")
            
            st.subheader("✨ Skills")
            skills = data.get('skills', [])
            if skills:
                for skill in skills:
                    st.write(f"**{skill.get('skillName', 'Unknown')}** - Nível {skill.get('level', 1)}")
            else:
                st.write("Sem skills")
            
            armor_set = data.get('armorSet')
            if armor_set and armor_set.get('bonus'):
                st.subheader("🎯 Set Bonus")
                st.write(armor_set['bonus'].get('name', 'Unknown'))
        
        elif recurso == "items":
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("⭐ Raridade")
                st.write(f"{data.get('rarity', 'N/A')}")
            
            with col2:
                st.subheader("📦 Limite")
                st.write(f"{data.get('carryLimit', 'N/A')}")
            
            with col3:
                st.subheader("💰 Valor")
                st.write(f"{data.get('value', 'N/A')}")
            
            st.subheader("📝 Descrição")
            st.write(data.get('description', 'Sem descrição'))
            
            crafting = data.get('crafting')
            if crafting:
                st.subheader("🔨 Crafting")
                materiais = crafting.get('craftingMaterials', []) or crafting.get('materials', [])
                if materiais:
                    for mat in materiais:
                        item = mat.get('item', {})
                        qtd = mat.get('quantity', 1)
                        st.write(f"- {item.get('name', 'Unknown')} x{qtd}")
        
        elif recurso == "weapons":
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("⚔️ Tipo")
                st.write(data.get('type', 'N/A').replace('-', ' ').title())
            
            with col2:
                st.subheader("⭐ Raridade")
                st.write(f"{data.get('rarity', 'N/A')}")
            
            with col3:
                st.subheader("💥 Ataque")
                attack = data.get('attack', {})
                st.write(f"**Display:** {attack.get('display', 'N/A')}")
                st.write(f"**Raw:** {attack.get('raw', 'N/A')}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🎯 Afinidade")
                affinity = data.get('affinity')
                if affinity is not None:
                    st.write(f"{affinity}%")
                else:
                    st.write("N/A")
            
            with col2:
                st.subheader("🔘 Slots")
                slots = data.get('slots', [])
                if slots:
                    st.write(f"{len(slots)} slot(s)")
                    for slot in slots:
                        st.write(f"- Nível {slot.get('rank', 1)}")
                else:
                    st.write("Sem slots")
            
            st.subheader("✨ Elementos")
            elements = data.get('elements', [])
            if elements:
                for elem in elements:
                    st.write(f"- {elem.get('type', 'Unknown').capitalize()} ({elem.get('damage', 0)})")
            else:
                st.write("Sem elementos")
            
            st.subheader("🔨 Crafting")
            crafting = data.get('crafting', {})
            
            if crafting.get('craftable'):
                st.write("✅ Craftável")
            else:
                st.write("❌ Não craftável")
            
            materiais = crafting.get('craftingMaterials', [])
            if materiais:
                st.write("**Materiais:**")
                for mat in materiais:
                    item = mat.get('item', {})
                    qtd = mat.get('quantity', 1)
                    st.write(f"- {item.get('name', 'Unknown')} x{qtd}")
            
            branches = crafting.get('branches', [])
            if branches:
                st.write(f"**Upgrade para:** {len(branches)} arma(s)")
        
        with st.expander("📄 Ver dados técnicos completos (JSON)"):
            st.json(data)
    
    else:
        st.warning(f"⚠️ '{nome}' não encontrado em {recurso_selecionado}.")
        st.info("Dica: Verifique se o nome está escrito corretamente ou tente buscar em outra categoria.")

# ============================================================
# RODAPÉ
# ============================================================
st.divider()
st.caption(f"🐉 Hunter Codex - Dados da MHW-DB API | Cache: MongoDB | Recurso atual: {recurso_selecionado}")