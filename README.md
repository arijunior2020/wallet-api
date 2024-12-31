# Wallet API

## Descrição
API para criar e gerenciar carteiras digitais com suporte a CRUD, depósitos, saques e transferências.

## Endpoints Principais
- `POST /wallets`: Criar uma nova carteira.
- `GET /wallets/{id}`: Obter detalhes de uma carteira.
- `PUT /wallets/{id}`: Atualizar uma carteira.
- `DELETE /wallets/{id}`: Excluir uma carteira.
- `POST /wallets/{id}/deposit`: Depositar na carteira.
- `POST /wallets/{id}/withdraw`: Sacar da carteira.
- `POST /wallets/transfer`: Transferir entre carteiras.

## Como Executar
1. **Localmente:**
   ```bash
   python -m app.app
