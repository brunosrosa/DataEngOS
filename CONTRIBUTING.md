# Contributing to DataEngOS

Bem-vindo ao DataEngOS! Estamos felizes em ter você conosco. Este guia detalha como configurar seu ambiente para desenvolvimento e como contribuir com o projeto.

---

## ⚡ Configuração Rápida (Setup)

### Pré-requisitos
- **Linux** (ou WSL2 no Windows).
- **Python 3.10** ou superior.
- **Permissões de Sudo** (apenas para instalar o `python3-venv` na primeira execução).

### Automação
Se você estiver com pressa, rode nosso script de setup:

```bash
chmod +x scripts/setup_dev.sh
./scripts/setup_dev.sh
```

### O que o script faz?
1. Checa se o Python 3 está instalado.
2. Checa (e instala via `apt`) o módulo `python3-venv`.
3. Cria um ambiente virtual em `.venv`.
4. Instala o pacote em modo editável (`pip install -e .`).

---

## 🛠 Comandos Úteis

Após configurar, ative o ambiente:
```bash
source .venv/bin/activate
```

### Validar um Contrato
O comando `validate` garante que o YAML segue o padrão ODCS v2.2.
```bash
dataeng-os validate projects/<PROJETO>/contracts/inputs/<ARQUIVO>.yaml
```

### Gerar Código (Scaffold)
O comando `scaffold` lê um contrato e gera modelos dbt (SQL e YML) documentados.
```bash
dataeng-os scaffold dbt projects/<PROJETO>/contracts/inputs/<ARQUIVO>.yaml
# O output será gerado automaticamente em projects/<PROJETO>/dbt/staging/
```

---

## 🧩 Estrutura do Repositório

- `core/`: O "cérebro" do sistema (Lógica agnóstica, Governança, Prompts).
- `dataeng_os/`: O código fonte Python do CLI.
- `projects/`: Onde vivem os projetos de dados reais.
- `scripts/`: Utilitários de automação e DevOps.

---

## 🤝 Como Contribuir

1. **Issues:** Antes de codar, abra uma Issue descrevendo o problema ou feature.
2. **Branching:** Use o padrão `feat/<nome>` ou `fix/<nome>`.
3. **Pull Request:** Descreva suas mudanças e garanta que `dataeng-os validate` passe nos contratos de exemplo.

Dúvidas? Fale com o **DataEngOS Architect**.
