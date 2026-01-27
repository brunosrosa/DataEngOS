# Privacy & LGPD Policy

## 1. Objetivo

Garantir que todos os pipelines de dados estejam em conformidade com a LGPD (Lei Geral de Proteção de Dados) desde a concepção (Privacy by Design).

## 2. Classificação de Dados

Os dados devem ser classificados conforme `core/global_governance/classification.yaml`:

- **Público**: Dados abertos.
- **Interno**: Dados corporativos não sensíveis.
- **Confidencial**: Dados estratégicos.
- **Restrito (PII)**: Dados pessoais identificáveis.

## 3. Tratamento de PII

- **Identificação**: Campos PII devem ser taggeados no catálogo e nos contratos.
- **Mascaramento**: Obrigatório na camada Silver em diante para usuários sem credencial específica.
- **Anonimização**: Para ambientes de desenvolvimento e pré-produção.
- **Exclusão (Right to be Forgotten)**: Pipelines devem suportar expurgo de dados de titulares.

## 4. Retenção

- Todo dataset deve ter política de retenção definida no contrato ou plano do projeto.
- Logs de acesso a dados sensíveis devem ser mantidos por 5 anos.
