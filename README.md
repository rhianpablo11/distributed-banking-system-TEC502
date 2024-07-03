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

Algumas questões, relacionadas com concorrencia, foram encontradas no desenvolvimento do projeto, e que necessitaram de soluções cabiveis a cada uma delas. Essas questões se encontravam com a manipulação de um mesmo dado, visto que por o servidor ser configurado como multithread, logo mais de um thread poderia realizar a alteração de um dado ao mesmo tempo, gerando conflitos. Outro problema relacionado com a concorrencia, esta presente nas operações sobre uma mesma conta em que - explicar problema q fez precisar usar o token ring

Visando solucionar o primeiro problema, uma opção encontrada foi o uso do objeto "lock", que é disponibilizado pela biblioteca Threading do python. Esse objeto possui dois métodos, um responsavel por "adquirir" o "lock", e o outro responsavel por "soltar" o "lock". Com isso foi possivel implementa-lo nas operações em que envolvem adição de dados, ou manipulação dos dados salvos. Tendo em vista que na linha de codigo em que é colocado para realizar a "adquirição" do "lock", caso ele não esteja disponivel, o programa fica preso naquela linha, saindo apenas quando o lock é liberado por "quem havia adquirido". Com isso por mais que varios threads tentem alterar o dado, eles tem de esperar um "soltar" o lock para outro operar, ficando apenas uma operação por vez sendo executada. Neste projeto o "lock" foi utilizado dentro das contas, ou seja cada conta possui o seu proprio "lock", e com isso antes de realizar alguma operação é primeiro requerido o "lock", para após realizar a operação e ao final da mesma o "lock" é devolvido, e fica disponivel para outras operações serem realizadas.

Em busca de uma solução em que permitisse ordenar os eventos, e permitir que apenas um realize a operação por vez, é que foi utilizado o algoritmo do token ring. Este algoritmo utiliza uma topologia do tipo anel, em que um token percorre por todos os hosts presentes na rede. Quando o host possui alguma operação a ser feita este aguarda por o token chegar ate ele para realizar, ao finalizar essa ação ele coloca o token na rede novamente. Originalmente, essa metodologia pode gerar problemas, tendo em vista o risco de um host ser desconectado e todo os outros ficarem esperando a reconexão deste para conseguir seja, passar o token que estava com ele, ou para fechar o anel e permitir a passagem do token, com ele recebendo o token e passando para o proximo host. Pensando nessas questões que adaptações na implementação foram feitas para um melhor funcionamento.


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

### Comunicação

Para realizar a comunicação entre os servidores dos bancos, bem como permitir que esses servidores sejam acessados pela interface, seja para requisição de dados ou inserir dados, foi utilizado uma API no padrão REST, a qual faz uso do protocolo HTTP. Para auxiliar na criação da API foi feito uso do framework Flask, desenvolvido para linguagem python. Ademais, também foi feito uso da biblioteca requests, desenvolvido para liguagem python. Esta permite realizar requests para a API, e receber os dados do retorno, o que foi essencial para permitir a troca de mensagens interna entre os bancos. Com isso, a comunicação se divide em duas partes: servidor-interface, e servidor-servidor.

#### Comunicação servidor-servidor
A comunicação entre servidores tem dois principais usos, realizar o envio do token para o outro servidor, para que ele com o token possa realizar uma operação, e para enviar uma requisição para o outro servidor realizar a operação requisitada pelo cliente. Esta ultima situação ocorre quando o usuário possui conta em mais de um banco, e este deseja enviar um montante de dinheiro que está na sua conta em outro banco. Sendo assim para poder opera precisa o banco em que ele esta logado enviar uma requisição autorizada para o outro banco poder realizar a operação.

A primeira situação de comunicação, para envio do token, é uma das mais importantes, já que cada servidor bancario, só realiza uma operação quando possui o token. Ao receber o token, o servidor faz uma busca na lista de operações para executar, caso ainda tenha operação a ser feita, é realizado uma operação e passado o token, caso não tenha nenhuma operação a ser realizada, o token é passado.

A comunicação entre os bancos ocorre em rotas especificas, em que são utilizadas apenas entre os bancos. As rotas, os dados em que esperam receber em cada rota, e o dado em que retornam esta presente na Tabela [Rotas de comunicação interna aos bancos](#rotas-de-comunicação-internas-aos-bancos)

Vale ressaltar a questão da confiabilidade para comunicação entre os bancos.
-falar da questão de quando vai tentar realizar uma operação
-falar da questao de quando vai transferir o token
-falar da questao de quando nao precisa dessa confiabilidade
--operações de deposito nao precisa

#### Comunicação servidor-interface

A comunicação  realizada entre o servidor e a interface, ocorre com um contrato de comunicação mais simples do que ocorre na comunicação entre os bancos. Tendo em vista que a interface, envia dados para o servidor do banco em especifico, afim deste realizar operações monetarias para aquela conta, ou para criação de uma conta. Ademais a interface faz diversos requests de dados para o servidor, com o objetivo de apresentar valores atualizados na interface em que o usuario esta logado.

Para estabelecer essa comunicação entre eles, é feito uso de requisições para as rotas especificas em que a interface envia dados para o servidor. Essas rotas podem ser vistas na tabela [Rotas de comunicação com a interface](#rotas-de-comunicação-com-a-interface).

Afim facilitar o papel do servidor ao identificar o tipo de transação e como ela deve operar, foi desenvolvido um padrão nas requisições de operar dados, em que elas devem possuir no json uma especie de cabeçalho com informações basicas e logo após os dados para realizar aquela operação. Um exemplo de como deve estar os dados:
```javascript
{
    "operation": "create"/"deposit"/"sendPix"/"packetPix",
    "clientCpfCNPJ": "111.111.111-11",
    "dataOperation":{
        "aqui estao os dados presentes para realizar cada operação"
    }
}
```

Para operações de **criar conta**, o padrão de dado esperado pelo servidor é:
```javascript
"dataOperation": {
    "name1": "nome do usuario principal",
    "cpfCNPJ1": "cpf/cnpj do usuario principal",
    "name2": "preenchido com o nome do usuario associado a conta, caso seja conta conjunta",
    "cpfCNPJ2": "preenchido com o cpf/cnpj do usuario associado a conta, caso seja conta conjunta",
    "email": "email do usuario",
    "password":"senha da conta",
    "telephone": "numero de telefone do usuario",
    "isFisicAccount": "indica se a conta é de pessoa fisica ou de empresa",
    "isJoinetAccount": "indica se a conta é conjunta ou não"
}

```

Para operação de **realizar um deposito**, o padrão de dado esperado pelo servidor é:
```javascript
"dataOperation": {
    "value": "valor do deposito",
    "method": "metodo em que foi depositado, seja dinheiro/qr code/boleto bancario"
}
```

Para operação de **enviar um pix**, o padrão de dado esperado pelo servidor é:
```javascript
"dataOperation": {
    "value": "valor a ser enviado",
    "keyPix": "chave pix do cliente que receberá",
    "idBank": "ID do banco onde o cliente possui aquela chave",
    "bankNameReceiver":"nome do banco que irá receber o dinheiro",
    "nameReceiver": "nome de quem esta recebendo o dinheiro"
}
```
Para operação de **enviar um pacpte de pix**, o padrão de dado esperado pelo servidor é:
```javascript
"dataOperation": [
    {
        "value": "valor a ser enviado",
        "keyPix": "chave pix do cliente que receberá",
        "idBank": "ID do banco onde o cliente possui aquela chave",
        "nameReceiver": "nome de quem esta recebendo o dinheiro",
        'bankSourceMoney': "nome do banco que irá sair o dinheiro"
    },
    {
        "value": "valor a ser enviado",
        "keyPix": "chave pix do cliente que receberá",
        "idBank": "ID do banco onde o cliente possui aquela chave",
        "nameReceiver": "nome de quem esta recebendo o dinheiro",
        'bankSourceMoney': "nome do banco que irá sair o dinheiro"
    }, ...
]
    

```

### ServerBank

-falar do lock

### AccountModel

O accountModel é uma classe em que foi pensada como um dos pontos centrais no quesito de realizar as transações. Diante disso, o servidor do banco ao receber uma requisição de deposito, por exemplo, verifica a existencia daquela conta no banco de dados, e existindo chama o metodo daquela classe para poder realizar o deposito. Dessa forma fica separado cada função, o servidor fica responsavel por coordenar as operações e mante-las em ordem, e o objeto da classe, é quem fica encarregado de colocar, retirar ou enviar dinheiro para outra conta, ou para a propria.

Ainda vale ressaltar que com o uso dessa classe é possivel construir um dicionario contendo informações sobre esse usuario para ser enviado para a interface, ou para enviar dados parciais sobre o usuario quando requisitado as informações dele para realizar a transferencia via pix. Este dicionario é convertido num objeto json antes de ser enviado. Isso permite a interface ser apresentar os dados para o usuário de forma mais visivel e informativa.

Cabe citar ainda a presença de um objeto lock, da biblioteca Threading do python. Este tem a serventia de controlar as multiplas operações que podem ocorrer envolvendo aquela mesma conta naquele banco. Com a presença do lock, apenas uma operação de mudança de dados é executada por vez, em ordem de chegada, já que ao ser "adquirido" um lock, outra operação a ser realizada por outro thread tem que aguardar o lock ser "solto" para ele pegar e realizar a operação. Dessa maneira a concorrencia interna de alteração de dados fica solucionada.

### TransactionModel

O transactionModel é uma classe, em que visa simplificar o armazenamento de dados sobre cada operação, e com isso consegue realizar um melhor controle sobre aquela conta. Tal controle permite facilitar o "roll back" das transações em que ocorrem erro, ou realizar a confirmação da transação.

Entre os dados que cada transação possui, o seu status, o valor da transação, o tipo da transação - indicar se foi envio, recebimento, ou deposito de dinheiro - são informações importantes para a operação. Ao realizar uma operação em que envolve mais de uma conta, a transação é adicionada na lista presente na conta, contudo com o status "pending", e é retornado o ID daquela operação. Ao fim da operação, o banco responsavel por enviar o dinheiro envia outra requisição novamente para informar a conclusão, ou informar o erro na operação, e a partir do ID é possível acessar a transação, alterar o seu status para concluida, ou para que deu error, e retirar o dinheiro da parte de saldo bloqueado, para a parte o saldo comum, em caso de operação confirmada, ou para nenhum local em caso de erro.


#### Algoritmo Token Ring

Um dos contratempos do projeto, ocorre com a questão de concorrencia de operações, situação decorrente de multiplas operações sobre uma mesma conta, e envolvendo ela, poderem ser disparadas para executar ao mesmo tempo. Sem controlar a ordem dessas operações, multiplos erros poderiam ocorrer, podendo resultar em duplo gasto, trasanções sendo enviadas sem o usuario possuir dinheiro, entre outros casos de erro.

Sobe esse viés, em que o algoritmo Token Ring foi implmentado, visando permitir que as operações sejam executadas em cada banco apenas quando ele estiver com o token. Cada banco possui sua fila de transações, e a cada passagem do token por aquele banco, apenas uma operação é executada. Isso traz maior performance pensando num conjunto, e é uma forma de dividir o tempo igualmente entre os servidores dos bancos, já que ao permitir um banco realizar toda a sua fila de operações antes de passar o token, os outros bancos seriam prejudicados por um tempo maior de espera para realizar as suas operações proprias.

O token, trafega entre os bancos carregando dados consigo que servem para melhora da confiabilidade do sistema. Esses dados fazem parte da adaptação do algoritmo, afim de evitar que a desconexão de um host afete o trafego do token, e em consequencia afetando os outros servidores de banco, que ficariam ativos na rede contudo sem poder operar por não estarem com o token. Dentre os dados enviados, estão o ID do servidor que esta enviado o token para o proximo servidor da fila, além de um *Array* contendo um contador de passagens do token por aquele servidor, neste *Array* estão presentes os valores de todos os host.

O sistema ao ser iniciado, o host com ID atribuido igual a "1", é o indicado para por o token na rede, para isso é definido que este possui o token, e graças a um thread que fica ativo sempre verificando se possui o token para, em caso positivo, procurar por uma operação ainda não realizada, e caso não tenha nenhuma operação esse mesmo thread chama a função que será responsavel pela passagem do token. Nesta algumas operações ocorrem, como verificação de para qual host ele irá tentar mandar o token, além de preencher os dados que serão enviados. Ao saber qual é o proximo host, ou seja o host que esta ao seu lado esperando para receber, é feita uma tentiva de passar o token, contudo caso não seja possível efetivar essa passagem, por o outro host ter sido desconectado, é então feita uma tentativa com o proximo do proximo, e por ai em diante até conseguir enviar para alguem. Nesse momento, há uma verificação para impedir que ele envie para ele mesmo o token, ou seja quando chega na vez de enviar para ele mesmo, ele reinicia o loop para enviar para o seu proximo. Caso somente este host esteja ativo na rede, ele permanece em loop tentando enviar para algum outro host.

Um dos sistemas para evitar que dois tokens estejam circulando na rede é o uso do *Array* com o valor da quantidade de passagens do token por aquele host. Esse sistema funciona com ao receber um token, o servidor verifica o valor presente na sua posição do *Array*, se esse valor for igual ao que ele possui atualmente, ou se for maior, o servidor aceita o token, adiciona um no valor presente na sua posição do *Array* e salva este consigo, e passa para frente ele já com o valor atualizado. Caso o servidor receba um token, que contém um *Array* e na sua posição esta um valor inferior, isso significa que quem está enviando foi desconectado, e o token foi posto na rede novamente, logo o valor do servidor foi incrementado, enquanto o que caiu ficou com o *Array* desatualizado. Nesse ultimo caso, é retornado para o servidor que foi desconectado, a informação sobre isso, e ele fica aguardando para que o token passe por ele novamente, e ele possa atualizar o *Array* para propagar um valor atualizado.

Outra proteção contra quedas de hosts, está presente com um temporizador para saber quando o token deve passar por ele novamente. Este tempostizador é iniciado no momento em que o token é passado e aguarda por 30 segundos, caso não recebe o token nesse tempo, é feita uma verificação com o host que lhe mandaou o token para conferir a atividade deste na rede. Tal verificação tem como objetivo evitar por um token na rede sem necessidade, gerando problemas por ter 2 tokens. As verificações com o host anterior ocorrem até 3 vezes, logo caso o host anterior passe 90 segundos, 30 segundos entre cada verificação, sem enviar o token, um novo token é posto na rede. Caso a verificação falhe, é definido que este servidor possui o token, e ele irá passar o token para frente.

Diante de todas essas verificações, 


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

A interface apresenta todas as operações em q 

## Testes


## Conclusão

## Referencias
> - [1] Python Software Foundation. Python Documentation. Biblioteca Threading. Versão 3.12. Disponível em: https://docs.python.org/3/library/threading.html. Acesso em: 29 maio 2024.
> - [2] Flask . Flask Documentation. Versão 3.0. Disponível em: https://flask.palletsprojects.com/en/3.0.x/#. Acesso em: 20 abril 2024.
> - [3] Battisti, Matheus. "React Router: O guia completo para navegação em aplicativos React". matheus Battisti - hora de Codar. Publicado em: 17 janeiro 2023. Disponível em: https://www.youtube.com/watch?v=7b42lVMdEjE. Acesso em: 30 maio 2024.
> - [4] DOCKER. Docker Documentation. Disponível em: https://docs.docker.com/. Acesso em: 20 junho 2024.
> - [5] KENNEDY, Kenneth Reitz. Requests: HTTP for Humans. Disponível em: https://requests.readthedocs.io/en/latest/#. Acesso em: 23 maio 2024.
