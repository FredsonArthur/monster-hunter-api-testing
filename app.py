import streamlit as st
import pandas as pd
import requests
from services.monster_service import MonsterService

# Inicializa o serviço
service = MonsterService(requests.Session(), "https://mhw-db.com")

# Configuração da página
st.set_page_config(page_title="Hunter Codex", layout="wide")
st.title("🏹 Hunter Codex Dashboard")

# ============================================================
# SIDEBAR - Configurações
# ============================================================
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Seletor de recurso
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
    
    # Refresh option
    force_refresh = st.checkbox("🔄 Ignorar cache (buscar da API)", value=False)
    
    st.divider()
    st.caption(f"Cache ativo para todos os recursos")
    st.caption(f"MongoDB: {'Conectado' if service.mongo_available else 'Offline (usando só API)'}")

# ============================================================
# ÁREA PRINCIPAL - Busca
# ============================================================
col1, col2 = st.columns([3, 1])

with col1:
    nome = st.text_input(
        f"🔍 Digite o nome do {recurso_selecionado.lower()}:",
        placeholder="Ex: Great Jagras, Potion, Leather Headgear..."
    )

with col2:
    st.write("")
    st.write("")
    buscar = st.button("🔍 Buscar", type="primary", use_container_width=True)

# ============================================================
# RESULTADOS
# ============================================================
if buscar and nome:
    with st.spinner(f"Buscando {nome} em {recurso_selecionado}..."):
        data = service.get_by_name(recurso, nome, force_refresh=force_refresh)
    
    if data:
        st.success(f"✅ {recurso_selecionado} encontrado: **{data.get('name')}**")
        
        # ====================================================
        # EXIBIÇÃO ESPECÍFICA POR TIPO DE RECURSO
        # ====================================================
        
        if recurso == "monsters":
            # MONSTROS
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
            
            # Resistências
            st.subheader("🛡️ Resistências")
            resistances = data.get('resistances', [])
            if resistances:
                for r in resistances:
                    cond = f" ({r.get('condition')})" if r.get('condition') else ""
                    st.write(f"**{r.get('element', 'Unknown').capitalize()}**{cond}")
            else:
                st.write("Nenhuma resistência listada")
            
            # Locais
            st.subheader("📍 Locais")
            locations = data.get('locations', [])
            if locations:
                for loc in locations:
                    st.write(f"- {loc.get('name', 'Unknown')}")
            else:
                st.write("Nenhum local listado")
        
        elif recurso == "ailments":
            # AILMENTS (Status)
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
            # ARMADURAS
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
            
            # Skills
            st.subheader("✨ Skills")
            skills = data.get('skills', [])
            if skills:
                for skill in skills:
                    st.write(f"**{skill.get('skillName', 'Unknown')}** - Nível {skill.get('level', 1)}")
            else:
                st.write("Sem skills")
            
            # Set Bonus
            armor_set = data.get('armorSet')
            if armor_set and armor_set.get('bonus'):
                st.subheader("🎯 Set Bonus")
                st.write(armor_set['bonus'].get('name', 'Unknown'))
        
        elif recurso == "items":
            # ITENS
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
            
            # Crafting (se aplicável)
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
            # ARMAS
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
            
            # Afinidade e slots
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
            
            # Elementos
            st.subheader("✨ Elementos")
            elements = data.get('elements', [])
            if elements:
                for elem in elements:
                    st.write(f"- {elem.get('type', 'Unknown').capitalize()} ({elem.get('damage', 0)})")
            else:
                st.write("Sem elementos")
            
            # Crafting tree
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
            
            # Upgrade path
            branches = crafting.get('branches', [])
            if branches:
                st.write(f"**Upgrade para:** {len(branches)} arma(s)")
        
        # ====================================================
        # DADOS BRUTOS (expansível)
        # ====================================================
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