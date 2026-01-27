# Security & Access Policy

## 1. Controle de Acesso (RBAC)

- O acesso é concedido com base na necessidade (Least Privilege).
- Roles padrão:
  - `data_producer`: Leitura/Escrita em seus domínios.
  - `data_consumer`: Leitura na camada Gold de domínios permitidos.
  - `admin`: Gerenciamento da plataforma.

## 2. Autenticação

- Integração obrigatória com SSO corporativo.
- Service Accounts para pipelines, com rotação automática de chaves.

## 3. Segregação de Ambientes

- **DEV**: Dados mockados ou anonimizados. Acesso livre para desenvolvedores.
- **STG**: Réplica de produção anonimizada. Testes de integração.
- **PROD**: Dados reais. Acesso restrito (Break-glass access apenas).

## 4. Auditoria

- Todas as queries e acessos a dados devem ser logados.
- Alterações de schema e permissões devem passar por code review (GitOps).
