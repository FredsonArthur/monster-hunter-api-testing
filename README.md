## 📋 Cobertura de Testes e Estratégia
Nossa suíte é estruturada para cobrir os pilares fundamentais de qualidade de software, utilizando **Mocks** para garantir isolamento, velocidade e independência de rede:

| Categoria | Descrição |
| :--- | :--- |
| **Smoke Tests** | Validação de conectividade e saúde dos endpoints via mock. |
| **Schema Validation** | Garantia da conformidade do contrato de dados (JSON) via `jsonschema`. |
| **Data-Driven Testing** | Parametrização para testes escaláveis de múltiplos recursos. |
| **Performance** | Monitoramento de latência e tempos de resposta em ambiente controlado. |
| **Security Fuzzing** | Testes de robustez contra entradas inválidas sem dependência externa. |

## 🛡️ O Diferencial: Blindagem Local (Hunter Codex)
O **Hunter Codex** não depende mais de conexão com o servidor da MHW-DB API para executar sua bateria de testes. Implementamos:
* **Interceptação de Requisições:** Uso de `requests-mock` em todos os testes, eliminando falhas por instabilidade de rede.
* **Fixtures Locais:** Todos os dados da API são armazenados em `tests/fixtures/`, permitindo testes determinísticos.
* **Automação de Dados:** Script utilitário em `scripts/fetch_fixtures.py` que mantém a base local sincronizada com a API real quando necessário.
* **Validação de Schema:** Testes avançados que garantem que, mesmo com dados mockados, a estrutura do JSON permanece íntegra.

---