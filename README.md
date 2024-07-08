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


A execução do projeto utiliza, conforme requisitado, o docker como ferramenta para criação de containers e execução dos mesmos. Considerando a necessidade dos servidores dos bancos estarem conectados na mesma rede, além dos containers, foi criada uma rede interna ao docker. Essa operação foi automatizada ao criar um docker compose, em que com um comando todo o sistema fica ativo.


###  Procedimento para a primeira execução
1. Realizar o clone do repositorio para uma pasta local, executando o seguinte comando no terminal:
    ``` bash
      git clone https://github.com/rhianpablo11/distributed-banking-system-TEC502.git
    ```
2. Acesse a pasta do projeto executando o comando abaixo:
    ``` bash
      cd .\distributed-banking-system-TEC502\
    ```
3. Execute o seguinte comando para construir as imagens, e a network e executar os containers:
    ```  bash
      docker compose up --build
    ```


### Procedimento para execuções subsequentes
1. Acesse a pasta do projeto pelo terminal
2. Execute o seguinte comando para executar os containers:
```  bash
    docker compose up
```


### Procedimento para execução em computadores diferentes
1. Acesse a pasta do projeto
2. Abra o documento [docker-compose.yaml](https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/main/docker-compose.yaml)
3. Altere o endereço IP de cada um dos hosts, exceto o daquele próprio host. Por exemplo, para o serviço de ID 4, não precisa alterar o endereço próprio dele, apenas o dos outros.
   1. Exemplo da alteração:
        ``` yaml
            environment:
                - HOST_1=172.16.103.14
                - HOST_2=172.16.103.10
                - HOST_3=192.168.0.13
                - HOST_4=172.16.103.12
                - HOST_5=172.16.103.13
                - ID=3
        ```
4. Execute o seguinte comando para executar os containers:
```  bash
    docker compose up "nome do banco a ser executado" --build
```

## Sumario
1. [Introdução](#introdução)
2. [Fundamentação Teórica](#fundamentação-teórica)
3. [Metodologia](#metodologia)
4. [Implementação](#implementação)
   1. [Estrutura do projeto]()
      1. [Comunicação servidor-servidor]()
      2. [Comunicação servidor-interface]()
      3. [Rotas de comunicação internas aos bancos]()
      4. [Rotas de comunicação com a interface]()
   3. [Middleware]()
   4. [AccountModel]()
   5. [TransactionModel]()
   6. [Algoritmo Token Ring]()
   7. [Operações]()
      1. [Criação de conta]()
      2. [Deposito]()
      3. [Enviar Pix]()
      4. [Enviar pacote de Pix]()
   8. [Interface]()
5. [Testes](#testes)
6. [Conclusão](#conc)
7. [Referências]()


## Introdução


O desenvolvimento tecnológico é algo que está cada vez mais presente na vida das pessoas, e isso permite se integrar em diferentes áreas trazendo facilidades no cotidiano. Uma dessas facilidades está presente no contexto bancário, com a criação de um novo tipo de transferência, o Pix. Esta solução permite realizar movimentações para outras contas, seja no mesmo banco ou em bancos diferentes, ocorrendo de forma quase instantânea e simples para o usuário.


Contudo essa solução desenvolvida e implementada no Brasil, conta com um sistema centralizado ao seu favor, já que o país possui o Banco Central. Pensando no sucesso e funcionalidade do Pix é que o governo de um país sem banco central, se interessou em desenvolver um sistema semelhante ao presente no Brasil. Essa solução tem de contemplar o fato de ser distribuída, já que o país em questão não possui um ponto centralizado, possibilitando a comunicação entre os bancos presentes no *consórcio bancário*. Os bancos presentes nessa solução tem de se portar de forma comum, permitindo o gerenciamento das contas pelos clientes, transferências atômicas entre as contas nos bancos, e criação de pacotes com várias transferências para serem realizadas de uma só vez.


Pensando em atender aos requisitos, algumas soluções foram necessárias para o desenvolvimento a fim de permitir o funcionamento dos bancos distribuidamente, sem a presença de um ponto central. Neste documento são encontradas mais informações sobre a questão da concorrência, sincronização e comunicação entre os bancos, tratamento de confiabilidade, realização do pacote de transações, e como essas questões foram solucionadas e implementadas. Na tabela [Topicos princiais do documento](#topicos-pricipais-do-documento) estão disponiveis alguns assuntos importantes relativos ao processo, e o(s) tópico(s) relacionado(s).

<div align=center>

### Topicos pricipais do documento

| Assunto                                                     | Topicos                 |
| :---------------------------------------------------------- | :-----------------------|
| Gerenciamento de contas, criação e realização de transações | [Operações](#operações) |
| Transação entre contas e entre bancos | [Operações](#operações), [Enviar Pix](#enviar-pix), [Enviar pacote Pix ](#enviar-pacote-de-pix) |
| Comunicação entre servidores | [Comunicação](#comunicação), [Comunicação Servidor-servidor](#comunicação-servidor-servidor) |
| Sincronização no mesmo servidor | [Operações](#operações), [Comunicação](#comunicação) |
| Algoritmo de concorrencia distribuida | [Algoritmo Token Ring](#algoritmo-token-ring) |
| Tratamento de confiabilidade | [Algoritmo Token Ring](#algoritmo-token-ring),[Operações](#operações), [Criar conta](#criação-de-conta), [Enviar Pix](#enviar-pix), [Enviar pacote Pix ](#enviar-pacote-de-pix)|
| Transação concorrente | [Operações](#operações), [Algoritmo Token Ring](#algoritmo-token-ring) |

</div>

## Fundamentação teórica


O projeto em questão possui alguns pontos principais, que foram tratados ao longo do desenvolvimento. Dentre estes pontos se encontram a criação de um único servidor, em que este pode ser instanciado mais de uma vez, e realizando a comunicação entre as suas instâncias para troca de mensagens. Sendo assim, cada servidor, a depender do ID atribuído a ele, representa um dos bancos presentes no consórcio.


Algumas questões, relacionadas com concorrencia, foram encontradas no desenvolvimento do projeto, e que necessitaram de soluções cabíveis a cada uma delas. Essas questões se encontravam com a manipulação de um mesmo dado, visto que por o servidor ser configurado como multithread, logo mais de um thread poderia realizar a alteração de um dado ao mesmo tempo, gerando conflitos. Outro problema relacionado com a concorrência, está presente em operações que possam gerar bloqueio, por uma conta esperar resposta de outra, e a outra esperar resposta de uma terceira que esta envolvendo a segunda e a primeira. Nesta situação as contas ficam esperando resposta de alguma, mas travadas sem conseguir operar.


Visando solucionar o primeiro problema, uma opção encontrada foi o uso do objeto *lock*, que é disponibilizado pela biblioteca Threading do python. Esse objeto possui dois métodos, um responsável por "adquirir" o *lock*, e o outro responsável por "soltar" o *lock*. Com isso foi possível implementá-lo nas operações em que envolvem adição de dados, ou manipulação dos dados salvos. Tendo em vista que na linha de código em que é colocado para realizar a aquisição do *lock*, caso ele não esteja disponível, o programa fica preso naquela linha, saindo apenas quando o*locké* liberado por "quem havia adquirido". Com isso, por mais que várias threads tentem alterar o dado, eles têm de esperar um "soltar" o*lockpara* outro operar, ficando apenas uma operação por vez sendo executada. Neste projeto o *lock* foi utilizado dentro das contas, ou seja cada conta possui o seu próprio *lock*, e com isso antes de realizar alguma operação é primeiro requerido o *lock*, para após realizar a operação e ao final da mesma o *lock* é devolvido, e fica disponível para outras operações serem realizadas.


Em busca de uma solução em que permitisse ordenar os eventos, e permitir que apenas um realize a operação por vez, é que foi utilizado o [algoritmo do token ring](#algoritmo-token-ring). Este algoritmo utiliza uma topologia do tipo anel, em que um token percorre por todos os hosts presentes na rede. Quando o host possui alguma operação a ser feita este aguarda por o token chegar até ele para realizar, ao finalizar essa ação ele coloca o token na rede novamente. Originalmente, essa metodologia pode gerar problemas, tendo em vista o risco de um host ser desconectado e todo os outros ficarem esperando a reconexão deste para conseguir seja, passar o token que estava com ele, ou para fechar o anel e permitir a passagem do token, com ele recebendo o token e passando para o próximo host. Pensando nessas questões, que adaptações na implementação foram feitas para um melhor funcionamento.


Não menos importante, também foi implementado o protocolo *2 Phase Commit* para as transações que envolvem mais de uma conta, seja no mesmo banco ou em bancos diferentes. Esse protocolo opera em duas diferentes fases da transação, sendo a primeira direcionada para a preparação entre os envolvidos para realizar a operação, e após os dois estarem preparados, é executada a segunda fase, direcionada à confirmação da transação. Essa confirmação pode servir para permitir confirmar esta, ou para requisitar o cancelamento por algum erro ocorrido durante o processo de preparação.




## Metodologia


A Fim de realizar o desenvolvimento do projeto, cumprindo com os requisitos exigidos pelo problema, tornou-se essencial a aplicação dos conceitos teóricos presentes na seção [Fundamentação teórica](#fundamentação-teórica) na implementação. Uma das principais questões para ser resolvida estava presente na concorrência entre os servidores, e como solucionar para evitar inconsistência de dados durante as transações. Tal concorrência presente seja na modificação interna do mesmo dado por mais de um thread, ou por múltiplos bancos requisitando uma transação sobre a mesma conta no mesmo banco para eles. Considerando tais questões que o uso do algoritmo de token ring foi utilizado, bem como o uso do *lock*.


Vale ressaltar ainda o uso da ferramenta *Docker*, para possibilitar a criação de containers em que estes rodam em ambientes separados. Sendo assim, foi utilizado de outra ferramenta do *Docker* o *Docker compose*, este que possibilita criar os 6 container necessários para essa aplicação de forma simplificada, tanto no momento de construção, bem como para definir as variáveis de ambiente. Os 5 últimos containers criados, representam cada um dos bancos, e o primeiro container representa a interface.


## Implementação


### Estrutura do projeto
- [**`Interface`**](#interface):
  - Responsável por permitir que os usuários criem, ou façam login em suas contas no banco escolhido. Além disso, é possível realizar operações na sua conta, seja ela presente no banco ao qual se conectou, ou operando sobre o dinheiro presente em outro banco.
  - Desenvolvido utilizando a framework "React Js" para o JavaScript
- [**`Middleware`**](#middleware):
  - Responsável por receber requisições provindas da interface, e dos outros bancos e realizar o devido retorno correto dos dados. Além disso ele é responsável por armazenar os dados das contas bancárias presentes nele, e controlar a ordem das operações a serem realizadas.
  - Desenvolvido utilizando a linguagem Python
- [**`AccountModel`**](#accountmodel):
  - Classe responsável por controlar os dados relacionados a conta bancária, armazenando cada dado em seu atributo específico para facilitar os futuros resgate de dados, além de realizar operações internas a ela, como realização de depósitos, envio de dinheiro ou recebimento.
  - Desenvolvido utilizando a linguagem Python
- [**`TransactionModel`**](#transactionmodel):
  - Classe responsável por armazenar os dados relacionados à transação, para facilitar manipulações sobre ela, como por exemplo realizar a reversão de uma operação em que ocorreu um erro.
  - Desenvolvido utilizando a linguagem Python


### Comunicação


Para realizar a comunicação entre os servidores dos bancos, bem como permitir que esses servidores sejam acessados pela interface, seja para requisição de dados ou inserir dados, foi utilizado uma API no padrão REST, a qual faz uso do protocolo HTTP. Para auxiliar na criação da API foi feito uso do framework Flask, desenvolvido para linguagem python. Ademais, também foi feito uso da biblioteca requests, desenvolvido para linguagem python. Esta permite realizar requests para a API, e receber os dados do retorno, o que foi essencial para permitir a troca de mensagens interna entre os bancos. Com isso, a comunicação se divide em duas partes: servidor-interface, e servidor-servidor. Vale ressaltar que o framework Flask consegue trabalhar com multithreads, logo multiplas requisições podem chegar ao mesmo momento para serem processadas.


#### Comunicação servidor-servidor
A comunicação entre servidores tem dois principais usos, realizar o envio do token para o outro servidor, para que ele com o token possa realizar uma operação, e para enviar uma requisição para o outro servidor realizar a operação requisitada pelo cliente. Esta última situação ocorre quando o usuário possui conta em mais de um banco, e este deseja enviar um montante de dinheiro que está na sua conta em outro banco. Sendo assim, para poder operar precisa o banco em que ele está logado enviar uma requisição autorizada para o outro banco poder realizar a operação.


A primeira situação de comunicação, para envio do token, é uma das mais importantes, já que cada servidor bancário, só realiza uma operação quando possui o token. Ao receber o token, o servidor faz uma busca na lista de operações para executar, caso ainda tenha operação a ser feita, é realizado uma operação e passado o token, caso não tenha nenhuma operação a ser realizada, o token é passado.


A comunicação entre os bancos ocorre em rotas específicas, em que são utilizadas apenas entre os bancos. As rotas, os dados em que esperam receber em cada rota, e o dado em que retornam esta presente na Tabela [Rotas de comunicação interna aos bancos](#rotas-de-comunicação-internas-aos-bancos)


Vale ressaltar a questão da confiabilidade para comunicação entre os bancos. Essa necessária para impedir erros nas transações decorrentes quedas de rede em algum dos bancos. Algoritmos para permitir essa confiabilidade estão implementados no [algoritmo do token ring](#algoritmo-token-ring) utilizado, bem como na [realização das operações](#operações).




#### Comunicação servidor-interface


A comunicação  realizada entre o servidor e a interface, ocorre com um contrato de comunicação mais simples do que ocorre na comunicação entre os bancos. Tendo em vista que a interface, envia dados para o servidor do banco em especifico, a fim deste realizar operações monetárias para aquela conta, ou para criação de uma conta. Ademais a interface faz diversos requests de dados para o servidor, com o objetivo de apresentar valores atualizados na interface em que o usuario esta logado.


Para estabelecer essa comunicação entre eles, é feito uso de requisições para as rotas específicas em que a interface envia dados para o servidor. Essas rotas podem ser vistas na tabela [Rotas de comunicação com a interface](#rotas-de-comunicação-com-a-interface).


Afim facilitar o papel do servidor ao identificar o tipo de transação e como ela deve operar, foi desenvolvido um padrão nas requisições de operar dados, em que elas devem possuir no json uma espécie de cabeçalho com informações básicas e logo após os dados para realizar aquela operação. Um exemplo de como deve estar os dados:
```javascript
{
    "operation": "create"/"deposit"/"sendPix"/"packetPix",
    "clientCpfCNPJ": "111.111.111-11",
    "dataOperation":{
        "aqui estão os dados presentes para realizar cada operação"
    }
}
```


Para operações de [**criar conta**](#criação-de-conta), o padrão de dado esperado pelo servidor é:
```javascript
"dataOperation": {
    "name1": "nome do usuário principal",
    "cpfCNPJ1": "cpf/cnpj do usuário principal",
    "name2": "preenchido com o nome do usuário associado a conta, caso seja conta conjunta",
    "cpfCNPJ2": "preenchido com o cpf/cnpj do usuário associado a conta, caso seja conta conjunta",
    "email": "email do usuário",
    "password":"senha da conta",
    "telephone": "número de telefone do usuário",
    "isFisicAccount": "indica se a conta é de pessoa física ou de empresa",
    "isJoinetAccount": "indica se a conta é conjunta ou não"
}


```


Para operação de [**realizar um depósito**](#deposito), o padrão de dado esperado pelo servidor é:
```javascript
"dataOperation": {
    "value": "valor do depósito",
    "method": "método em que foi depositado, seja dinheiro/qr code/boleto bancário"
}
```


Para operação de [**enviar um pix**](#enviar-pix), o padrão de dado esperado pelo servidor é:
```javascript
"dataOperation": {
    "value": "valor a ser enviado",
    "keyPix": "chave pix do cliente que receberá",
    "idBank": "ID do banco onde o cliente possui aquela chave",
    "bankNameReceiver":"nome do banco que irá receber o dinheiro",
    "nameReceiver": "nome de quem está recebendo o dinheiro"
}
```
Para operação de [**enviar um pacote de pix**](#enviar-pacote-de-pix), o padrão de dado esperado pelo servidor é:
```javascript
"dataOperation": [
    {
        "value": "valor a ser enviado",
        "keyPix": "chave pix do cliente que receberá",
        "idBank": "ID do banco onde o cliente possui aquela chave",
        "nameReceiver": "nome de quem está recebendo o dinheiro",
        'bankSourceMoney': "nome do banco que irá sair o dinheiro"
    },
    {
        "value": "valor a ser enviado",
        "keyPix": "chave pix do cliente que receberá",
        "idBank": "ID do banco onde o cliente possui aquela chave",
        "nameReceiver": "nome de quem está recebendo o dinheiro",
        'bankSourceMoney': "nome do banco que irá sair o dinheiro"
    }, ...
]
```


<div align="center">


  #### Rotas de comunicação internas aos bancos


  | Rotas                             | Metodo | Retorno                                                                                                                                                                                                                                                             | Dado recebido                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
  | :-------------------------------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
  | "/token"                          | POST   | Retorna ok, código 200, caso o valor do token recebido esteja de acordo com a regra *REFERENCIA A PARTE DA REGRA. Caso não esteja de acordo retorna o código 405                                                                                                    | Objeto Json, contendo a informação do host que está enviado o dado, e a lista atualizada do token. Exemplo do dado esperado: {"nodeSender": "1", "tokenIDList": [0,0,0,0,0]}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
  | "/verify-conection"               | GET    | Retorna ok, código 200, caso esteja ativo. No caso em que não está ativo na rede ele não recebe a requisição                                                                                                                                                        | None                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
  | "/search-account"                 | POST   | Retorna ok, código 200, caso a conta do cliente exista naquele banco, caso não exista retorna informando isso com o código 404                                                                                                                                      | Objeto Json contendo o nome do banco que fez a pesquisa, além do CPF/CNPJ ao qual está procurando. Exemplo do dado esperado: {"cpfCNPJ1": "111.111.111-11", "bankName": "Eleven"}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
  | "/account/pix"                    | POST   | Retorna, caso o cliente exista naquele banco, informações básicas, como nome, nome do banco, cpf/CNPJ parcialmente escondido, sobre aquela conta, caso aquela conta não exista é retornado que o cliente não existe naquele banco                                   | Objeto json contendo a chave pix (cpf/cnpj do cliente). Exemplo do dado esperado: {"keyPix": "111.111.111-11"}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
  | "/account/receive-pix"            | PATCH  | Retorna, caso o cliente exista naquele banco, um objeto contendo o ID da transação de receber dinheiro que foi operada naquela conta, e uma mensagem informando o sucesso                                                                                           | Objeto Json contendo a autorização, que indica que quem pediu está com o token, a chave pix (cpf/cnpj do cliente), o nome de quem está enviando o dinheiro e seu CPF/CNPJ, o valor a ser enviado, o nome do banco em que está saindo o dinheiro, o nome de quem receberá, e o nome do banco que receberá. Exemplo do dado esperado: {'authorization': True, 'nameSender': "João Luiz", 'cpfCNPJSender': "111.111.111-11", 'value': 30000, 'bankSourceName': "Eleven", 'keyPix': "222.222.2222-22", 'nameReceiver': "Jose Gonçalves", 'bankNameReceiver': "Automobili"}                                                                                                                |
  | "/account/send-pix"               | POST   | Retorna, caso o cliente exista e a transação tenha ocorrido tudo bem, o ID da transação da conta que enviou o dinheiro, e o ID da transação na conta que recebeu o dinheiro, caso a transação não tenha sido possível de realizar é enviado o devido codigo de erro | Objeto Json contendo a autorização, que indica que quem pediu está com o token, a chave pix (cpf/cnpj do cliente), o nome de quem está enviando o dinheiro e seu CPF/CNPJ, o valor a ser enviado, o nome do banco em que está saindo o dinheiro, o nome de quem receberá, e o nome do banco que receberá, e a url para qual com qual banco ele vai enviar o dinheiro. Exemplo do dado esperado: {'authorization': True, 'nameSender': "João Luiz", 'cpfCNPJSender': "111.111.111-11", 'value': 30000, 'bankSourceName': "Eleven", 'keyPix': "222.222.2222-22", 'nameReceiver': "Jose Gonçalves", 'bankNameReceiver': "Automobili", 'url': "http://localhost:8081/account/receive-pix} |
  | "/account/confirmation-operation" | POST   | Retorna ok, caso a transação tenha sido confirmada com sucesso, caso ocorra algum erro e não seja confirmada, é enviado o devido codigo de erro                                                                                                                     | Objeto json contendo a autorização para realizar a operação, alem do CPF/CNPJ da conta que deseja confirmar a operação, adjunto ao ID da transação naquela conta. Exemplo de dado esperado: {'cpfCNPJ': "111.111.111-11", 'idTransaction': 2, 'authorization': True}                                                                                                                                                                                                                                                                                                                                                                                                                  |
  | "/account/error-transaction"      | POST   | Retorna ok, caso a transação tenha sido confirmada o erro, caso não tenha sido possível marcar aquela transação com erro, o código de erro é retornado                                                                                                              | Objeto json contendo a autorização para realizar a operação, além do CPF/CNPJ da conta que deseja confirmar a operação, adjunto ao ID da transação naquela conta. Exemplo de dado esperado: {'cpfCNPJ': "111.111.111-11", 'idTransaction': 2, 'authorization': True}                                                                                                                                                                                                                                                                                                                                                                                                                  |




  #### Rotas de comunicação com a interface
  | Rotas                               | Método | Retorno                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Dado recebido                                                                                                                                                                   |
  | :---------------------------------- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
  | "/operations"                       | POST   | Retorna uma informação a depender do tipo de operação escolhido, sendo possível enviar a operação de: criar conta, enviar dinheiro, depositar dinheiro, enviar um pacote contendo várias transações de enviar dinheiro. Caso a operação seja criação de conta, o retorno pode ser os dados sobre aquela conta criada, ou uma mensagem de erro sobre a criação. Caso a operação seja de enviar dinheiro ou de depositar, o retorno será se foi concluída com sucesso a operação ou não. Caso a operação seja de enviar um pacote contendo várias transações de enviar dinheiro, o retorno será se elas aconteceram ok, ou se uma delas der erro, é informado esse erro | None                                                                                                                                                                            |
  | "/bank"                             | GET    | Retorna o nome do banco, ao qual fez a requisição                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Objeto json contendo informação sobre qual operação será realizada, o CPF/CNPJ do cliente, e os dados da operação.                                                              |
  | "/account/login"                    | POST   | Retorna o conjunto de dados do cliente, caso ele exista naquele banco, por meio de um objeto json. Em caso contrário é retornado o devido código e mensagem de erro.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Objeto json contendo o email que o cliente usou para fazer registro, adjunto a sua senha. Exemplo do dado esperado: {"email": "josemiguel@hotmail.com", "password": "12345678"} |
  | "/account/data/<int:accountNumber>" | GET    | Retorna o conjunto de dados daquela conta ao qual foi passado pela url no request, caso não exista aquele número de conta é retornado que a conta não existe                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | None                                                                                                                                                                            |
  | "/account/transaction/pix/infos"    | POST   | Retorna as informações básicas da conta ao qual foi passada a chave Pix, caso a conta não exista, ou seja passada a chave com um ID de banco invalido, é retornado a mensagem de erro, junto ao código de erro                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Objeto json contendo o ID do banco a qual quer fazer a requisição e a chave Pix que está procurando. Exemplo de dado esperado: {"idBank": "1", "keyPix": "111.111.111-11"}      |


  </div>






### [Middleware](https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/main/server/middleware.py)


Este componentedo projeto é responsável por coordenar todas as operações e possibilitar a comunicação seja [servidor-servidor](#comunicação-servidor-servidor), ou [servidor-interface](#comunicação-servidor-interface). Para coordenar as operações em paralelo ao receber requisições, foi ativado no Flask, framework para utilizado para construção da API, o modo *threaded*, em que ele opera com multiplos threads. Outros 2 threads são fixos, sendo um deles mantendo a função que verifica a presença do token, para possível execução de uma operação, caso haja alguma ainda não executada na fila, e por fim passar o token para o proximo servidor. O outro thread se responsabiliza em manter o temporizador ativo, para detectar se o tempo limite para receber o token novamente foi atingido ou não.


### [AccountModel](https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/main/server/accountModel.py)


O accountModel é uma classe em que foi pensada como um dos pontos centrais no quesito de realizar as transações. Diante disso, o servidor do banco ao receber uma requisição de depósito, por exemplo, verifica a existência daquela conta no banco de dados, e existindo chama o método daquela classe para poder realizar o depósito. Dessa forma fica separado cada função, o servidor fica responsável por coordenar as operações e mantê-las em ordem, e o objeto da classe, é quem fica encarregado de colocar, retirar ou enviar dinheiro para outra conta, ou para a própria.


Ainda vale ressaltar que com o uso dessa classe é possível construir um dicionário contendo informações sobre esse usuário para ser enviado para a interface, ou para enviar dados parciais sobre o usuário quando requisitado as informações dele para realizar a transferência via pix. Este dicionário é convertido num objeto json antes de ser enviado. Isso permite a interface ser apresentar os dados para o usuário de forma mais visível e informativa.


Cabe citar ainda a presença de um objeto *lock*, da biblioteca Threading do python. Este tem a serventia de controlar as múltiplas operações que podem ocorrer envolvendo aquela mesma conta naquele banco. Com a presença do *lock*, apenas uma operação de mudança de dados é executada por vez, em ordem de chegada, já que ao ser "adquirido" um *lock*, outra operação a ser realizada por outro thread tem que aguardar o *lock* ser "solto" para ele pegar e realizar a operação. Dessa maneira a concorrência interna de alteração de dados fica solucionada.


### [TransactionModel](https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/main/server/transactionModel.py)


O transactionModel é uma classe, em que visa simplificar o armazenamento de dados sobre cada operação, e com isso consegue realizar um melhor controle sobre aquela conta. Tal controle permite facilitar o "roll back" das transações em que ocorrem erros, ou realizar a confirmação da transação.


Entre os dados que cada transação possui, o seu status, o valor da transação, o tipo da transação - indicar se foi envio, recebimento, ou depósito de dinheiro - são informações importantes para a operação. Ao realizar uma operação em que envolve mais de uma conta, a transação é adicionada na lista presente na conta, contudo com o status "pending", e é retornado o ID daquela operação. Ao fim da operação, o banco responsável por enviar o dinheiro envia outra requisição novamente para informar a conclusão, ou informar o erro na operação, e a partir do ID é possível acessar a transação, alterar o seu status para concluida, ou para que deu erro, e retirar o dinheiro da parte de saldo bloqueado, para a parte o saldo comum, em caso de operação confirmada, ou para nenhum local em caso de erro.




### Algoritmo Token Ring


Um dos contratempos do projeto, ocorre com a questão de concorrência de operações, situação decorrente de múltiplas operações sobre uma mesma conta, e envolvendo ela, poderem ser disparadas para executar ao mesmo tempo. Sem controlar a ordem dessas operações, erros poderiam ocorrer como por exemplo um banco A iniciar uma operação que envolve uma conta no banco B, e o banco C realizar uma operação nessa mesma conta no banco B requisitando enviar algo para a primeira conta citada, no banco A, porém esta ultima estará travada esperando resposta da conta no banco B, enquanto essa conta também está travada esperando uma resposta provinda do banco A. Com isso, torna-se essencial coordenar a ordem operacional dos bancos, afim de evitar situações como esta já que ao coordenar as operações, apenas um banco opera por vez impedindo esses bloqueios.


Sob esse viés, em que o algoritmo Token Ring foi implementado, visando permitir que as operações sejam executadas em cada banco apenas quando ele estiver com o token. Cada banco possui sua fila de transações, e a cada passagem do token por aquele banco, apenas uma operação é executada. Isso traz maior performance pensando num conjunto, e é uma forma de dividir o tempo igualmente entre os servidores dos bancos, já que ao permitir um banco realizar toda a sua fila de operações antes de passar o token, os outros bancos seriam prejudicados por um tempo maior de espera para realizar as suas operações próprias. E além disso se torna possível contornar o problema de concorrência entre as operações, já que elas são executadas conforme a ordem em que chegaram e foram adicionadas na fila, e somente uma por vez quando o banco está em posse do token. Logo as operações não operam em paralelo, mas sequencialmente tanto internamente ao banco, como externamente entre os bancos por conta do token.


O token, trafega entre os bancos carregando dados consigo que servem para melhora da confiabilidade do sistema. Esses dados fazem parte da adaptação do algoritmo, a fim de evitar que a desconexão de um host afete o tráfego do token, e em consequência afetando os outros servidores de banco, que ficariam ativos na rede contudo sem poder operar por não estarem com o token. Dentre os dados enviados, estão o ID do servidor que está enviando o token para o próximo servidor da fila, além de um *Array* contendo um contador de passagens do token por aquele servidor. Cada servidor do banco possui uma posição fixa nesse *Array* e é nessa posição em que o contador fica registrado, logo nele estão presentes os valores de todos os hosts. 


O sistema ao ser iniciado, o host com ID atribuído igual a "1", é o indicado para por o token na rede, para isso é definido que este possui o token, e graças a [uma thread](https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/1b99a3a42b620c8b03590befc6dd05987fdd0ce4/server/middleware.py#L1105) que fica ativa sempre verificando se possui o token para, em caso positivo, procurar por uma operação ainda não realizada, e caso não tenha nenhuma operação esse mesmo thread chama a [função que será responsável pela passagem do token](https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/3e54d1a7143a6eabdb20cb27a3c51ae98470f515/server/middleware.py#L418). Nesta algumas operações ocorrem, como verificação de para qual host ele irá tentar mandar o token, além de preencher os dados que serão enviados. Ao saber qual é o próximo host, ou seja o host que está ao seu lado esperando para receber, é feita uma tentativa de passar o token, contudo caso não seja possível efetivar essa passagem, por o outro host ter sido desconectado, é então feita uma tentativa com o próximo do próximo, e por aí em diante até conseguir enviar para alguém. Nesse momento, há uma verificação para impedir que ele envie para ele mesmo o token, ou seja quando chega na vez de enviar para ele mesmo, ele reinicia o loop para enviar para o seu próximo. Caso somente este host esteja ativo na rede, ele permanece em loop tentando enviar para algum outro host.


Um dos sistemas para evitar que dois tokens estejam circulando na rede é o uso do *Array* com o valor da quantidade de passagens do token por aquele host. Esse sistema funciona com ao receber um token, o servidor verifica o valor presente na sua posição do *Array*, se esse valor for igual ao que ele possui atualmente, ou se for maior, o servidor aceita o token, adiciona um no valor presente na sua posição do *Array* e salva este consigo, e passa para frente ele já com o valor atualizado. Caso o servidor receba um token, que contém um *Array* e na sua posição esteja um valor inferior, isso significa que quem está enviando foi desconectado, e um novo token foi posto na rede novamente, logo o valor do servidor foi incrementado, enquanto o que sofreu a desconecção ficou com o *Array* desatualizado. Nesse caso, é retornado para o servidor que foi desconectado, e tentou por o token na rede, a informação sobre isso, e ele fica aguardando para que o token passe por ele novamente, e ele possa atualizar o *Array* para propagar um valor atualizado.


Outra proteção contra quedas de hosts, está presente com um temporizador para saber quando o token deve passar por ele novamente. Este temporizador é iniciado no momento em que o token é passado e aguarda por 30 segundos somado ao seu valor de ID elevado ao quadrado - evitar o caso em que dois servidores detectem uma desconecção ao mesmo tempo e coloquem 2 tokens, um cada, na rede - caso não receba o token nesse tempo, é feita uma verificação com o host que lhe mandou o token para conferir a atividade deste na rede. Tal verificação tem como objetivo evitar por um token na rede sem necessidade, gerando problemas por ter 2 tokens. As verificações com o host anterior ocorrem até 3 vezes, com tempo fixo entre cada verificação, sem enviar o token, um novo token é posto na rede. Caso a verificação falhe, há outra etapa antes de gerar um novo token, está realiza a verificação com todos os hosts conhecidos, realizando um multicast, para verificar a atividade deles. Isso permite que o proprio servidor detecte se ele foi desconectado, já que se nenhum servidor responder, ele entende a sua desconexão e fica em *stand-by* aguardando. Caso ele ele detecte que ele está na rede junto a outros, então um novo token é gerado e enviado. Vale ressaltar que é somado 100 a todos as posições do *Array* antes de ser realizado o envio. 


Diante de todas essas verificações, é possível tornar o algoritmo "resistente" a quedas de conexão de algum dos hosts, seja o host que está com o token, ou com o que está aguardando o token.




### [Operações](https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/3e54d1a7143a6eabdb20cb27a3c51ae98470f515/server/middleware.py#L757)


A realização das operações é divida em partes, iniciando no recebimento da operação a ser executada e finalizando no retorno da requisição. Dentre as etapas estão, [receber a requisição](https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/1b99a3a42b620c8b03590befc6dd05987fdd0ce4/server/middleware.py#L144) e construir um dicionário contendo um os dados da requisição, contendo uma chave para ser preenchida com a resposta de retorno a ser retornada, e outra chave informando se está concluída ou não. Esses campos adicionais aos dados da operação são de importância para o controle sobre a requisição. A próxima etapa é [colocar a operação na fila](https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/3e54d1a7143a6eabdb20cb27a3c51ae98470f515/server/middleware.py#L1092), em que para isso é feito o uso do *lock*, a fim de evitar 2 requisições pedindo para colocar dados na fila ao mesmo tempo, o que geraria conflitos. Tal *lock* também é utilizado ao realizar alterações no dicionário presente na fila. A [penúltima etapa na realização da operação é realizá-la de fato](https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/3e54d1a7143a6eabdb20cb27a3c51ae98470f515/server/middleware.py#L481), sendo para cada tipo uma lógica diferente. Os tipos disponíveis são: criar conta, enviar pix, depósito e enviar um pacote de pix. Por último, com a operação concluída, é feito o retorno para quem requisitou.


#### [Criação de conta](https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/3e54d1a7143a6eabdb20cb27a3c51ae98470f515/server/middleware.py#L763)


A criação da conta, ocorre com o servidor primeiro realizando verificação da existência daquele cpf/cnpj  na base de dados como conta criada, e em caso positivo preenche o campo response da transação presente na fila,  e marca ela como concluída. Considerando que aquele cpf/cnpj ainda não está na base de dados, então é enviado um multicast para os bancos presentes no consórcio buscando saber se aquele cpf/cpnj possui conta neles. Essa operação busca manter a lista de bancos que o cliente possui conta atualizada. Os bancos que retornam informando que o cliente possui conta são postos na lista que irá ser usada na criação do objeto daquela conta, e cada um deles realiza a adição deste novo banco na sua lista. Caso nesse processo alguns bancos tenham sido desconectados, eles serão adicionados a uma lista para posterior verificação da presença neles daquele cpf/cnpj. Por fim é o objeto da classe Account é criado, e adicionado na base de dados do banco.




#### [Deposito](https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/3e54d1a7143a6eabdb20cb27a3c51ae98470f515/server/middleware.py#L817)


A operação de depósito é a mais simples, tendo em vista que é necessário apenas verificar aquele cpf/cnpj no banco em questão, e caso haja a conta é chamado um método da classe Account e este adiciona a transação de depósito. Por não envolver outros bancos, ele depende apenas da presença do token para realização.


#### [Enviar Pix](https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/3e54d1a7143a6eabdb20cb27a3c51ae98470f515/server/middleware.py#L830)


Esta operação é uma das mais complexas, por precisar preparar as contas envolvidas e após confirmar ou cancelar aquela operação. Para realizar isso primeiro é requisitado o método da classe Account para enviar o pix, nesse método será verificado se há saldo antes de realizar a operação. Com tudo nos conformes na conta de envio, ela envia para a rota “/receive-pix” no outro, ou no mesmo banco envolvido. Nesse momento ambos criam um objeto do tipo Trasanction, mas com o status pendente. Essa etapa corresponde a preparação entre os envolvidos e finalizada essa primeira etapa, o ID dessas transações, tanto para quem enviou como para quem recebeu será utilizado para enviar uma requisição pedindo que confirme ou cancele a operação. Nesse momento, há um envolvimento por um laço de repetição, para caso não consiga se comunicar com o outro host envolvido, continuar tentando até conseguir. Isso visa garantir a confiabilidade de finalizar aquela transação. Ademais, caso o host controlador da operação seja desconectado, ao ser conectado novamente ele continuará tentando enviar a requisição. Enquanto isso, todo o sistema daquele banco aguarda, já que essa etapa de confirmação ainda faz parte da operação.


#### [Enviar pacote de Pix](https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/3e54d1a7143a6eabdb20cb27a3c51ae98470f515/server/middleware.py#L871)


Para operar um pacote de transações, se assemelha com o [envio de pix](#enviar-pix), diferindo por executar uma fila dessas transações, além do adicional de poder pedir para outro banco enviar a transação no caso em que o banco de saída do dinheiro é diferente ao que recebe a operação. A operação inicia realizando uma transação do pacote por vez, e ao término é enviado para os envolvidos as tentativas de confirmação. Caso durante a realização de uma das transações ocorra erro, é então cancelada as próximas, e enviado para os envolvidos nas transações anteriores a requisição para cancelar a transação.




### [Interface](https://github.com/rhianpablo11/distributed-banking-system-TEC502/tree/3e54d1a7143a6eabdb20cb27a3c51ae98470f515/interface/bank-system-interface)


A interface desenvolvida para o projeto apresenta as funcionalidades disponíveis para uso do usuário, para que ele possa realizar o gerenciamento de sua conta de maneira mais interativa. Diante disso, ao abrir a tela inicial é requisitado o endereço do banco ao qual deseja se conectar, e a partir desse endereço é feito o redirecionamento à tela específica daquele banco. Na tela principal do banco o usuário consegue realizar a criação ou login em sua conta, para poder acessar a interface interna e realizar as suas operações.


A parte interna da interface, apresentada quando o usuário está logado, na *dashboard* contém informações sobre aquela conta, como saldo disponível, saldo bloqueado, lista das últimas transações, além de campo para realizar um depósito e realizar um pix rápido. Este último ocorrerá retirando o dinheiro da conta em que se está conectado. Outra tela presente internamente é a de *transactions*, em que possibilita a criação do pacote de transações para serem realizadas. Esse pacote de transações permite o usuário escolher de qual conta que ele possui irá ser retirado o dinheiro, e para quem e qual conta ele irá realizar o envio. Tal funcionalidade permite agilidade no processo, visto que multiplas transações de envio são montadas ao mesmo tempo, e sendo preciso realizar o pedido de realização apenas uma vez.

Ainda sobre a interface, cada banco possui o seu proprio nome e paleta de cores na interface interna, o que possibilita uma melhor diferenciação sobre qual banco esta sendo acessado e utilizado.




## Testes


A realização de testes foram essenciais para mediar o desenvolvimento, e verificar em cada etapa o funcionamento conforme esperado, e caso encontrado funcionamento diferente do esperado facilita a correção, visto o fato de ter encontrado previamente o erro. A execução destes testes iniciou das etapas mais simples, para posterior testes mais complexos e completos, em que envolvem desde as tarefas simples até as compostas.


A solução desenvolvida, conforme um dos requisitos, funciona utilizando comunicação http implementando uma API Rest. Sendo assim, para realização dos testes foi utilizado o programa PostMan, para criar as requisições, realizar o envio e verificar a resposta obtida pelo servidor.


Os primeiros testes iniciaram com as operações simples, envolvendo criação dos dados, como criação de conta, realização de login, requisição de dados básicos para apresentar ao realizar um pix. Estes testes podem ser vistos nas imagens 1, 2.

  <p align="center">
    <img width="" src="https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/3e54d1a7143a6eabdb20cb27a3c51ae98470f515/assets/cria%C3%A7%C3%A3o%20de%20conta%20-%20requisi%C3%A7%C3%A3o%20e%20resposta.png" />
    Img 1. Requisição de criar uma conta e o retorno obtido
  </p>
<p align="center">
    <img width="" src="https://github.com/rhianpablo11/distributed-banking-system-TEC502/blob/3e54d1a7143a6eabdb20cb27a3c51ae98470f515/assets/requisi%C3%A7%C3%A3o%20de%20dados%20previos%20para%20realizar%20o%20pix.png" />
    img 2. Requisição pedindo os dados pix da conta
  </p>

Testes envolvendo transações em ambiente controlado, sem a presença da concorrência entre os bancos e operações, ocorreram na sequência, para verificar as modificações nos saldos das contas, e as transações presentes na lista de cada conta, se estavam conforme esperado, sem presença de erros. Nessa etapa os testes de conectividade foram executados, visando testar a confiabilidade do sistema.


Ao obter a base do sistema construída e funcionando, tornou-se a vez de testar o algoritmo de concorrência. Inicialmente isolado das operações, verificando os casos em que um dos servidores é retirado da rede e após colocado, e como o sistema como um todo lidaria com isso. Conforme esperado e implementado, o token que percorre o sistema consegue "pular" para o próximo banco, caso o banco da vez não esteja na rede, outra situação é quando o banco que está com o token é desconectado, e nesse caso outro token é posto na rede, e quando o que foi desconectado tenta realizar envio do que estava consigo, ele é avisado sobre sua desconexão e fica aguardando o token passar novamente por ele. Os testes para este algoritmo foram facilitados com a ferramenta *docker*, ao construir uma network que permite a comunicação entre os containers, e realizar também a desconexão e reconexão de um container dessa rede, o que simularia retirar e depois colocar novamente o cabo de rede em um dos bancos. Além do *docker*, foi necessario utilizar a função *sleep()*, do modulo *sleep*, está funcionalidade que permite pausar o sistema pela quantidade de tempo definida, visando conseguir tempo para desconectar o container enquanto ele esta com o token, e sem o token.


Por fim, foi testado todo o sistema em conjunto utilizando das operações simples, mas com adição da concorrência, e adjunto várias operações sendo realizadas ao mesmo tempo. Consoante ao esperado no desenvolvimento, cada operação era realizada por vez em cada um dos bancos, sendo assim percebe-se o tratamento da concorrência. Testes de confiabilidade de desconexão também foram realizados, e conforme a implementação desenvolvida, houve funcionamento conforme esperado. Seja para cancelar operações, como para confirmação.


## Conclusão

Baseado no que foi apresentado, e o produto final obtido do desenvolvimento, observa-se que a conclusão do projeto foi um sucesso, ao atingir os requisitos que foram exigidos no problema. Dessa forma, a concorrencia entre os bancos foi tratada para evitar problemas e erros durante o uso do sistema, bem como a comunicação entre os bancos pra facilitar as transferencias nesse modelo bancario distribuído. Essas questões, operando com sistema de confiabilidade, tornando o sistema mais robusto e eficaz.

Não obstante, melhorias podem ser implementadas no projeto a fim de garantir tanto um sistema mais completo, como mais seguro. Dentre as melhorias, pode-se citar a segurança na comunicação entre servidor-interface, resolvendo isto ao utilizar token de autenticação nessa comunicação, bem como dados circulando na rede de maneira criptografada. Além disso, pode-se ainda implementar maior controle da conta, no quesito de realizar alterações no perfil do usuário.




## Referencias
> - [1] Python Software Foundation. Python Documentation. Biblioteca Threading. Versão 3.12. Disponível em: https://docs.python.org/3/library/threading.html. Acesso em: 29 maio 2024.
> - [2] Flask . Flask Documentation. Versão 3.0. Disponível em: https://flask.palletsprojects.com/en/3.0.x/#. Acesso em: 20 abril 2024.
> - [3] Battisti, Matheus. "React Router: O guia completo para navegação em aplicativos React". matheus Battisti - hora de Codar. Publicado em: 17 janeiro 2023. Disponível em: https://www.youtube.com/watch?v=7b42lVMdEjE. Acesso em: 30 maio 2024.
> - [4] DOCKER. Docker Documentation. Disponível em: https://docs.docker.com/. Acesso em: 20 junho 2024.
> - [5] KENNEDY, Kenneth Reitz. Requests: HTTP for Humans. Disponível em: https://requests.readthedocs.io/en/latest/#. Acesso em: 23 maio 2024.
> - [6] POSTMAN. Postman: API Platform for Building and Using APIs. Disponível em: https://www.postman.com/. Acesso em: 29 maio 2024.






