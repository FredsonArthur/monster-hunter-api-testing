# 🏹 Hunter Codex - Sistema de Consulta MHW-DB

[![CI Hunter Codex](https://github.com/SEU_USUARIO/SEU_REPOSITORIO/actions/workflows/testes.yml/badge.svg)](https://github.com/SEU_USUARIO/SEU_REPOSITORIO/actions/workflows/testes.yml)
[![Python Versions](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://python.org)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)]()
[![Coverage](https://img.shields.io/badge/Coverage-~70%25-yellow)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)](https://streamlit.io)
[![MongoDB](https://img.shields.io/badge/MongoDB-Cache-green)](https://mongodb.com)

## 📖 Sobre o Projeto

O **Hunter Codex** é um sistema completo de consulta à API do Monster Hunter World (MHW-DB), com:
- Dashboard interativo via **Streamlit**
- Cache persistente com **MongoDB**
- Suporte a **5 tipos de recursos**
- Testes automatizados com **Pytest**

## 🎯 Recursos Suportados

| Recurso | Descrição | Exemplo |
|---------|-----------|---------|
| 🐉 **Monstros** | Informações sobre monstros | Great Jagras, Rathalos |
| 💀 **Ailments** | Status e como curar/prevenir | Poison, Paralysis |
| 🛡️ **Armaduras** | Equipamentos e skills | Leather Headgear |
| 📦 **Itens** | Itens do jogo | Potion, Mega Potion |
| ⚔️ **Armas** | Armas e árvore de upgrade | Buster Sword 1 |

## 🛠️ Tecnologias

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![MongoDB](https://img.shields.io/badge/MongoDB-Cache-green)
![Pytest](https://img.shields.io/badge/Pytest-Tests-orange)

## 🚀 Como Executar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```
### 2. Iniciar MongoDB (opcional, para cache)
```bash

sudo systemctl start mongod
# ou
mongod
```
### 3. Rodar o Dashboard
```bash

streamlit run app.py
```
### 4. Rodar os Testes
```bash

pytest tests/ -v
```
### 📊 Estrutura do Projeto
```text

monster-hunter-api-testing/
├── app.py                    # Dashboard principal
├── pages/
│   └── health_dashboard.py   # Dashboard de saúde
├── services/
│   └── monster_service.py    # Lógica de busca e cache
├── tests/
│   ├── test_all_resources.py # Testes dos 5 recursos
│   ├── test_health.py        # Testes de saúde
│   └── fixtures/             # Dados mockados
├── scripts/
│   └── fetch_fixtures.py     # Coleta de fixtures
└── requirements.txt
```
### 🗄️ MongoDB - Estrutura do Cache

O sistema cria uma coleção por recurso:
```text

hunter_codex_db/
├── monsters/     # Monstros cacheados
├── ailments/     # Status cacheados
├── armor/        # Armaduras cacheadas
├── items/        # Itens cacheados
└── weapons/      # Armas cacheadas
```
### 🧪 Testes Disponíveis
```bash

# Todos os testes
pytest tests/ -v

# Testes específicos
pytest tests/test_all_resources.py -v
pytest tests/test_all_resources.py::TestAllResources -v

# Com relatório HTML
pytest --html=report.html
```
### 🔧 Configurações
Parâmetro	Padrão	Descrição
cache_ttl_hours	168 (7 dias)	Tempo de vida do cache
mongo_uri	mongodb://localhost:27017/	Conexão MongoDB
base_url	https://mhw-db.com	URL da API

👥 Desenvolvedores

    Fredson Arthur

    Eduarda Santos

    Thuanny Helen

📝 Licença

Este projeto é para fins educacionais e de estudo.