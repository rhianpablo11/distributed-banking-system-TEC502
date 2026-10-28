# Testes do Sistema Bancário Distribuído

Este diretório contém os scripts de teste de concorrência e carga do consórcio bancário distribuído.

## Scripts Disponíveis

### `concurrency_test.py`
Script multithread em Python que simula requisições concorrentes de clientes operando em paralelo contra os 5 nós bancários da rede:
1. **Criação de Contas**: Geração randômica de CPFs, nomes e contas, disparando threads simultâneas para cada banco.
2. **Depósito Simultâneo**: Realização concorrente de depósitos em dinheiro em todas as contas criadas.
3. **Transferências Pix Cruzadas**: Execução de transações Pix atômicas entre contas e nós distintos em paralelo, testando o algoritmo de exclusão mútua distribuída (**Token Ring**) e confirmação em duas fases (**Two-Phase Commit**).

### Como Executar

1. Certifique-se de que os containers do sistema estejam ativos:
   ```bash
   docker compose up -d
   ```

2. Instale a dependência de requisições (se necessário):
   ```bash
   pip install requests
   ```

3. Execute o script de teste:
   ```bash
   python tests/concurrency_test.py
   ```
   > Pressione `Enter` para aceitar os endereços padrão (`localhost:8081` a `localhost:8085`) ou informe os IPs/portas caso esteja testando em máquinas distribuídas.

