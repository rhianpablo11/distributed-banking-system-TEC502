# Coleções Postman

Este diretório contém as coleções de requisições HTTP para testes manuais e automatizados da API do consórcio bancário.

## Arquivos

1. **`bank_operations.postman_collection.json`**
   - Coleção principal de operações disponíveis para clientes e interface:
     - Criação de contas físicas e conjuntas
     - Autenticação e login
     - Depósitos de fundos
     - Consulta de saldo e dados cadastrais
     - Envio de Pix unitário
     - Envio de pacote em lote de transferências Pix (*Batch Pix*)

2. **`consortium_api.postman_collection.json`**
   - Coleção de chamadas internas da API de consórcio entre nós bancários:
     - Rotas de tráfego do Token (`/token`)
     - Verificação de heartbeat / conectividade (`/verify-conection`)
     - Busca distribuída de contas entre nós (`/search-account`)
     - Fases do Two-Phase Commit (`/account/receive-pix`, `/account/send-pix`, `/account/confirmation-operation`, `/account/error-transaction`)

## Como Utilizar no Postman

1. Abra o Postman.
2. Clique no botão **Import** (canto superior esquerdo).
3. Arraste ou selecione os arquivos JSON deste diretório.
4. Configure a variável de ambiente `hostPort` com a porta do nó desejado (ex.: `8081` para o *Eleven Bank*, `8082` para o *Automobili Bank*, etc.).

