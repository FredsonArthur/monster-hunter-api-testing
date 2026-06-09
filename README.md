# 🏹 Hunter Codex API Testing Suite

[![CI Hunter Codex](https://github.com/SEU_USUARIO/SEU_REPOSITORIO/actions/workflows/testes.yml/badge.svg)](https://github.com/SEU_USUARIO/SEU_REPOSITORIO/actions)

O **Hunter Codex** é uma suíte de automação de testes de API e dashboard de consulta desenvolvido para validar e interagir com a [MHW-DB API](https://mhw-db.com/). O projeto evoluiu para um ecossistema completo de engenharia de software com foco em resiliência e performance.

## 🛠 Tecnologias e Ferramentas
![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Pytest](https://img.shields.io/badge/Pytest-9.0-green?logo=pytest)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![SQLAlchemy](https://img.shields.io/badge/SQLite-Persistence-lightgrey?logo=sqlite)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-Automated-orange?logo=github)

---

## 🛡️ O Diferencial: Blindagem Local (Hunter Codex)
O projeto é 100% autossuficiente e independente de rede:
* **Interceptação:** Uso de `requests-mock` para testes determinísticos.
* **Persistência Híbrida:** Sistema de cache inteligente com **SQLite** para consultas rápidas e offline.
* **Validação:** Testes avançados de contrato via `jsonschema` e fuzzing de segurança.
* **Dashboard:** Interface interativa via **Streamlit** que consome o `MonsterService` localmente.

## 📋 Cobertura de Testes
Nossa suíte garante a integridade total do sistema:

| Categoria | Descrição |
| :--- | :--- |
| **Smoke Tests** | Saúde da API e conectividade. |
| **Schema Validation** | Conformidade dos contratos de dados (JSON). |
| **Data-Driven Testing** | Escalabilidade de testes parametrizados. |
| **Performance** | Monitoramento de latência em ambiente mockado. |
| **Security Fuzzing** | Robustez contra entradas inválidas/SQLi. |

## 👥 Desenvolvedores
* **Fredson Arthur**
* **Eduarda Santos**
* **Thuanny Helen**

---
## 🚀 Como Executar
1. Instale as dependências: `pip install -r requirements.txt`
2. Rode os testes com relatório HTML: `python -m pytest --html=report.html`
3. Inicie o dashboard: `streamlit run app.py`