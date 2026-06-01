# 🚀 Monster Hunter API Testing Suite

Este projeto é uma suíte de automação de testes de API desenvolvida com **Pytest** para validar a integridade, performance e robustez dos endpoints da [MHW-DB API](https://mhw-db.com/).

---

## 👥 Desenvolvedores
* **Fredson Arthur**
* **Eduarda Santos**
* **Thuanny Helen**

---

## 🛠 Tecnologias e Ferramentas
* **Python 3.x**
* **Pytest:** Framework principal de testes.
* **Requests:** Manipulação de requisições HTTP.
* **Jsonschema:** Validação de contratos de API.
* **Pytest-html:** Geração de relatórios visuais.

---

## 📋 Cobertura de Testes
Nossa suíte é estruturada para cobrir os pilares fundamentais de qualidade de software:

| Categoria | Descrição |
| :--- | :--- |
| **Smoke Tests** | Validação de conectividade e saúde dos endpoints. |
| **Schema Validation** | Garantia da conformidade do contrato de dados (JSON). |
| **Data-Driven Testing** | Parametrização para testes escaláveis de múltiplos monstros. |
| **Performance** | Monitoramento de latência e tempos de resposta. |
| **Security Fuzzing** | Testes de robustez contra entradas inválidas e maliciosas. |

---

## 🚀 Como Executar

### 1. Pré-requisitos
Certifique-se de ter o Python instalado. Recomendamos o uso de um ambiente virtual:

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Linux/macOS)
source venv/bin/activate