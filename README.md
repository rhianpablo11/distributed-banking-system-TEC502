<div align=center>

# Distributed Banking System
</div>

## Download do repositório

<div align='center'>
O download pode ser feito via clone do repositorio executando o seguinte comando no terminal:

``` bash
git clone https://github.com/rhianpablo11/distributed-banking-system-TEC502.git
```

</div>

## Como executar

A execução do projeto utiliza, conforme requisitado, o docker como ferramenta para criação de containers e execução dos mesmos. Considerando a necessidade dos servidores dos bancos estarem conectados na mesma rede, além dos containers foi criada uma rede interna ao docker. Essa operação foi automatizada* ao criar um docker compose, em que com um comando todo o sistema fica ativo.

### 1. Procedimento para a primeira execução
1. Acesse a pasta do projeto pelo terminal 
2. Execute o seguinte comando para construir as imagens, e a network e executar os containers:
```  bash
    docker compose up --build
```

### 1. Procedimento para execuções subsequentes
1. Acesse a pasta do projeto pelo terminal 
2. Execute o seguinte comando para executar os containers:
```  bash
    docker compose up
```

## Introdução

## Fundamentação teórica

O projeto em questão possui alguns pontos principais, que foram tratados ao longo do desenvolvimento. Dentre estes pontos se encontram a criação de um unico servidor, em que este pode ser instânciado mais de uma vez, e realizando a comunicação entre as suas instancias para troca de mensagens. Sendo assim, cada servidor, a depender do ID atribuido a ele, representa um dos bancos presente no consórcio. 

## Metodologia

## Implementação

### Estrutura do projeto
- [**`Interface`**](#):
  - Responsévael por permitir que os usuários criem, ou façam login em suas contas no banco escolhido. Além disso é possível realizar operações na sua conta, seja ela presente no banco ao qual se conectou, ou operando sobre o dinheiro presente em outro banco.
  - Desenvolvido utilizando a framework "React Js" para o JavaScript
- [**`ServerBank`**](#):
  - Responsável por receber requisições provindas da interface, e dos outros bancos e realizar o devido retorno correto dos dados. Além disso ele é responsavel por armazenar os dados das contas bancarias presentes nele, e controlar a ordem das operações a serem realizadas.
  - Desenvolvido utilizando a linguagem Python
- [**`AccountModel`**](#accountmodel):
  - Classe responsavel por controlar os dados relacionados a conta bancária, armazenando cada dado em seu atributo especifico para facilitar os futuros resgate de dados, além de realizar operações internas a ela, como realização de depositos, envio de dinheiro ou recebimento. 
  - Desenvolvido utilizando a linguagem Python
- [**`TransactionModel`**](#transactionmodel):
  - Classe responsavel por armazenar os dados relacionados a transação, para facilitar manipulações sobre ela, como por exemplo realizar a reversão de uma operação em que ocorreu um erro.
  - Desenvolvido utilizando a linguagem Python
### ServerBank

### AccountModel

### TransactionModel

#### Comunicação entre os bancos

#### Algoritmo Token Ring

<div align="center">

  #### Rotas de comunicação internas aos bancos

  | Rotas | Metodo | Retorno                   | Dado recebido                         |
  | :------- |:----------|:-------------------|:--------------------------|
  | "/token" | POST | Retorna ok, codigo 200, caso o valor do token recebido esteja de acordo com a regra *REFERENCIA A PARTE DA REGRA. Caso não esteja de acordo retorna o código 405| Objeto Json, contendo a informação do host que está enviado o dado, e a lista atualizada do token. Exemplo do dado esperado: {"nodeSender": "1", "tokenIDList": [0,0,0,0,0]}|
  | "/verify-conection" | GET | Retorna ok, codigo 200, caso esteja ativo. No caso em que não está ativo na rede ele não recebe a requisição | None|
  | "/search-account" | POST | Retorna ok, codigo 200, caso a conta do cliente exista naquele banco, caso não exista retorna informando isso com o codigo 404  | Objeto Json contendo o nome do banco que fez a pesquisa, além do CPF/CNPJ ao qual está procurando. Exemplo do dado esperado: {"cpfCNPJ1": "111.111.111-11", "bankName": "Eleven"}|
  | "/account/pix" | POST | Retorna, caso o cliente exista naquele banco, informações basicas, como nome, nome do banco, cpf/CNPJ parcialmente escondido, sobre aquela conta, caso aquela conta não exista é retornado que o cliente não existe naquele banco | Objeto json contendo a chave pix (cpf/cnpj do cliente). Exemplo do dado esperado: {"keyPix": "111.111.111-11"} |
  | "/account/receive-pix" | PATCH | Retorna, caso o cliente exista naquele banco, um objeto contendo o ID da transação de receber dinheiro que foi operada naquela conta, e uma mensagem informando o sucesso  | Objeto Json contendo a autorização, que indica que quem pediu esta com o token, a chave pix (cpf/cnpj do cliente), o nome de quem esta enviando o dinheiro e seu CPF/CNPJ, o valor a ser enviado, o nome do banco em que está saindo o dinheiro, o nome de quem receberá, e o nome do banco que receberá. Exemplo do dado esperado: {'authorization': True, 'nameSender': "João Luiz", 'cpfCNPJSender': "111.111.111-11", 'value': 30000, 'bankSourceName': "Eleven", 'keyPix': "222.222.2222-22", 'nameReceiver': "Jose Gonçalves", 'bankNameReceiver': "Automobili"}|
  | "/account/send-pix" | POST | Retorna, caso o cliente exista e a transação tenha ocorrido tudo bem, o ID da transação da conta que enviou o dinheiro, e o ID da transação na conta que recebeu o dinheiro, caso a transação não tenha sido possível de realizar é enviado o devido codigo de erro | Objeto Json contendo a autorização, que indica que quem pediu esta com o token, a chave pix (cpf/cnpj do cliente), o nome de quem esta enviando o dinheiro e seu CPF/CNPJ, o valor a ser enviado, o nome do banco em que está saindo o dinheiro, o nome de quem receberá, e o nome do banco que receberá, e a url para qual com qual banco ele vai enviar o dinheiro. Exemplo do dado esperado: {'authorization': True, 'nameSender': "João Luiz", 'cpfCNPJSender': "111.111.111-11", 'value': 30000, 'bankSourceName': "Eleven", 'keyPix': "222.222.2222-22", 'nameReceiver': "Jose Gonçalves", 'bankNameReceiver': "Automobili", 'url': "http://localhost:8081/account/receive-pix} |
  | "/account/confirmation-operation" | POST | Retorna ok, caso a transação tenha sido confirmada com sucesso, caso ocorra algum erro e não seja confirmada, é enviado o devido codigo de erro| Objeto json contendo a autorização para realizar a operação, alem do CPF/CNPJ da conta que deseja confirmar a operação, adjunto ao ID da transação naquela conta. Exemplo de dado esperado: {'cpfCNPJ': "111.111.111-11", 'idTransaction': 2, 'authorization': True}|
  | "/account/error-transaction" | POST | Retorna ok, caso a transação tenha sido confirmada o erro, caso não tenha sido possível marcar aquela transação com erro, o codigo de erro é retornado | Objeto json contendo a autorização para realizar a operação, alem do CPF/CNPJ da conta que deseja confirmar a operação, adjunto ao ID da transação naquela conta. Exemplo de dado esperado: {'cpfCNPJ': "111.111.111-11", 'idTransaction': 2, 'authorization': True}|


  #### Rotas de comunicação com a interface
  | Rotas | Metodo | Retorno                   | Dado recebido                         |
  | :------- |:----------|:-------------------|:--------------------------|
  | "/operations" | POST | Retorna uma informação a depender do tipo de operação escolhido, sendo possiveis enviar a operação de: criar conta, enviar dinheiro, depositar dinheiro, enviar um pacote contendo varias transações de enviar dinheiro. Caso a operação seja criação de conta, o retorno pode ser os dados sobre aquela conta criada, ou uma mensagem de erro sobre a criação. Caso a operação seja de enviar dinheiro ou de depositar, o retorno será se foi concluida com sucesso a operação ou não. Caso a operação seja de enviar um pacote contendo varias transações de enviar dinheiro, o retorno será se elas aconteceram ok, ou se uma delas der erro, é informado esse erro| None|
  | "/bank" | GET | Retorna o nome do banco, ao qual fez a requisição| Objeto json contendo informação sobre qual operação será realizada, o CPF/CNPJ do cliente, e os dados da operação.|
  | "/account/login" | POST | Retorna o conjunto de dados do cliente, caso ele exista naquele banco, por meio de um objeto json. Em caso contrario é retornado o devido codigo e mensagem de erro.| Objeto json contendo o email que o cliente usou para fazer registro, adjunto a sua senha. Exemplo do dado esperado: {"email": "josemiguel@hotmail.com", "password": "12345678"} |
  | "/account/data/<int:accountNumber>" | GET | Retorna o conjunto de dados daquela conta ao qual foi passado pela url no request, caso não exista aquele numero de conta é retornado que a conta não existe| None|
  | "/account/transaction/pix/infos" | POST | Retorna as informações basicas da conta ao qual foi passada a chave Pix, caso a conta não exista, ou seja passada a chave com um ID de banco invalido, é retornado a mensagem de erro, junto ao codigo de erro| Objeto json contendo o ID do banco a qual quer fazer a requisição e a chave Pix que está procurando. Exemplo de dado esperado: {"idBank": "1", "keyPix": "111.111.111-11"}|

  </div>



### Interface


## Testes


## Conclusão

## Referencias
> - [1] Python Software Foundation. Python Documentation. Biblioteca Threading. Versão 3.12. Disponível em: https://docs.python.org/3/library/threading.html. Acesso em: 29 maio 2024.
> - [2] Flask . Flask Documentation. Versão 3.0. Disponível em: https://flask.palletsprojects.com/en/3.0.x/#. Acesso em: 20 abril 2024.
> - [3] Battisti, Matheus. "React Router: O guia completo para navegação em aplicativos React". matheus Battisti - hora de Codar. Publicado em: 17 janeiro 2023. Disponível em: https://www.youtube.com/watch?v=7b42lVMdEjE. Acesso em: 30 maio 2024.
> - [4] DOCKER. Docker Documentation. Disponível em: https://docs.docker.com/. Acesso em: 20 junho 2024.
> - [5] KENNEDY, Kenneth Reitz. Requests: HTTP for Humans. Disponível em: https://requests.readthedocs.io/en/latest/#. Acesso em: 23 maio 2024.
