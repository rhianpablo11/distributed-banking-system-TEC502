
from hashlib import sha512
import socket
from flask_cors import CORS
from flask import *
import requests
from accountModel import Account
from utils import *

import threading
from time import sleep
import sys

addressBank = '0.0.0.0'
portBank = '8081'
selfID = "1"

global bankName
global accounts 
global listBanksConsortium
accounts = {}

accountsLock = threading.Lock()


listBanksConsortium = {
    "1": ["http://localhost:8081", "Eleven"],
    "2": ["http://localhost:8082", "Automobili"],
    "3": ["http://localhost:8083", "Secret"],
    "4": ["http://localhost:8084", "Formula"],
    "5": ["http://localhost:8085", "Titanium"]
}
print(os.getenv('HOST_1'))
ip1 = os.getenv('HOST_1')
ip2 = os.getenv('HOST_2')
ip3 = os.getenv('HOST_3')
ip4 = os.getenv('HOST_4')
ip5 = os.getenv('HOST_5')

listBanksConsortium["1"][0] = "http://"+os.getenv('HOST_1')+":8081"
listBanksConsortium["2"][0] = "http://"+os.getenv('HOST_2')+":8082"
listBanksConsortium["3"][0] = "http://"+os.getenv('HOST_3')+":8083"
listBanksConsortium["4"][0] = "http://"+os.getenv('HOST_4')+":8084"
listBanksConsortium["5"][0] = "http://"+os.getenv('HOST_5')+":8085"
print(listBanksConsortium)
print('IP DO PC: ', socket.gethostbyname(socket.gethostname()))

argumento =os.getenv('ID')
print(argumento)
selfID=argumento
if(argumento == "1" or argumento == "2" or argumento == "3" or argumento == "4" or argumento == "5"):
        
    value = listBanksConsortium[argumento][0]
    print(value)
    value=value.split(":")
    valueIP = ""
    valuePort = ""
    portBank = value[len(value)-1]
    if(argumento=="1"):
        addressBank = ip1
    if(argumento=="2"):
        addressBank = ip2
    if(argumento=="3"):
        addressBank = ip3
    if(argumento=="4"):
        addressBank = ip4
    if(argumento=="5"):
        addressBank = ip5


bankName = listBanksConsortium[selfID][1]
app = Flask(__name__)
CORS(app)
global hasToken
global operationOccurring
global previousNode
global nextNode
global timeOutTokenCounter
global initiateCouter
global tokenTimeOutSend
global requestPreviusNode
global tokenTimeOut
global tokenID
global disconnectionOcurred
global transactionsToMake
global transactionsToMakeID
global canPasstokenID
transactionsToMakeID = 0
transactionsToMake = {}
disconnectionOcurred = False
tokenID = [0,0,0,0,0]
addOperationLock = threading.Lock()
hasToken = False
hadToken = False
operationOccurring =  False
canPasstokenID = False
previousNode = int(selfID) - 1
if(previousNode == 0):
    previousNode=5

@app.route('/token', methods=['POST'])
def receiveToken():
    global hasToken
    global hadToken
    global operationOccurring
    global previousNode
    global tokenID
    global canPasstokenID
    global initiateCouter
    global counter 
    counter = 0
    initiateCouter = False
    infoReceived = request.json
    previousNode = infoReceived["nodeSender"]
    tokenIDNew = infoReceived["tokenIDList"]
    print("TOKEN QUE CHEGOU: ",tokenIDNew)
    print("TOKEN QUE TENHO:  ",tokenID)
    if((tokenIDNew[int(selfID)-1] >= tokenID[int(selfID)-1])):
        tokenID = tokenIDNew 
        tokenID[int(selfID)-1] +=1
        hasToken = True
        return "ok", 200
    else:
        tokenID[int(infoReceived["nodeSender"])-1] = 0
        return 'you were disconnected', 405


@app.route('/verify-conection', methods=['GET'])
def conectionTest():
    return "ok", 200


@app.route("/search-account", methods=['POST'])
def searchClient():
    dataReceived = request.json
    if(dataReceived['cpfCNPJ1'] in accounts):
        accounts[dataReceived['cpfCNPJ1']].addBankToList(dataReceived['bankName'])
        return 'user in the bank', 200
    else:
        return 'user not registed in the bank', 404

#aplicar o lock para essas operações, para que nao fique adicionando a torto e a direita e dar erro por ta mexendo no mesmo dicionario
@app.route('/operations', methods=['POST'])
def putOperationInList():
    dataReceived = request.json
    transactionsToMakeIDWaiting = putOperationInList(dataReceived)
    while (transactionsToMake[transactionsToMakeIDWaiting]["executed"]==False):
        pass   
    print(hasToken)
    return transactionsToMake[transactionsToMakeIDWaiting]["response"][0],transactionsToMake[transactionsToMakeIDWaiting]["response"][1]


@app.route('/accounts', methods=['GET'])
def getaccountsList():
    
    accountsList = []
    if(len(accounts) >0):
        for account in accounts:
            accountsList.append(accounts[account].jsonComplet())
    print(accountsList)
    print(accountsLock)
    response = make_response(jsonify(accountsList))
    response.headers['Cache-Control'] = 'private, max-age=1'

    return response


@app.route('/bank', methods=['GET'])
def getNameBank():
    dataSend = {
        "nameBank": listBanksConsortium[selfID][1]
    }
    response = make_response(jsonify(dataSend))
    return response, 200


'''
Função para realizar o login do usuario
'''
@app.route('/account/login', methods=['POST'])
def loginaccount():
    data =  request.json
    if(len(accounts) >0):
        for account in accounts:
            if(accounts[account].email == data["email"]):
                if(accounts[account].password == cryptographyPassword(data["password"])):
                    response = make_response(jsonify(accounts[account].jsonComplet()))
                    return response, 200
                else:
                    return "password incorrect", 401
        else:
            return "account not found", 404 
    else:
        return "account not found", 404    


@app.route('/account/data/<int:accountNumber>', methods=['GET'])
def getInfoAboutAccount(accountNumber):
    if(len(accounts) >0):
        for account in accounts:
            if(accounts[account].accountNumber == accountNumber):
                response = make_response(jsonify(accounts[account].jsonComplet()))
                return response, 200
                
        else:
            return "account not found", 404 
    else:
        return "account not found", 404 


"""
Função para procurar um accounte, e retornar dados basicos deste accounte
Esses dados são retornados para quem quer fazer o pix
"""
@app.route('/account/pix', methods=['POST'])
def getaccountPixInfo(): #fazer o retorno de informações basicas para apresentar na hora do pix
    data = request.json
    if(len(accounts) >0):
        if(data["keyPix"] in accounts):
            response = make_response(jsonify(accounts[data["keyPix"]].infoBasic()))
            return response
        else:
            return "account not found", 404
    else:
        return "account not found", 404


'''
Função para requisitar ao outro banco as informações do pix daquele usuario
'''
#PRECISA DE CORREÇÃO
@app.route('/account/transaction/pix/infos', methods=['POST'])
def getInfosForMakePix():
    data =  request.json
    if(data["bankID"] == "1" or data["bankID"] == "2" or data["bankID"] == "3" or data["bankID"] == "4" or data["bankID"] == "5"):
        url = listBanksConsortium[data["bankID"]][0]+"/account/pix"
        keyPix = {
            "keyPix": str(data["keyPix"])
        }
        infoReceived = requests.post(url,json=keyPix)
        if (infoReceived.status_code == 200):
            print(infoReceived.json())
            response = make_response(infoReceived.json())
            return response, 200
        else:
            print(infoReceived.status_code, infoReceived.text)
            return "Error in requisition",400              
    else:
        return "Bank invalid", 404


@app.route('/account/receive-pix', methods=['PATCH'])
def receiveMoneyWithPix():
    dataReceived = request.json
    if(len(accounts) == 0):
        return "account not found", 404
    elif(len(accounts)>0):
        if(dataReceived['authorization']):
            print(accounts)
            print(dataReceived['keyPix'])
            if(dataReceived['keyPix'] not in accounts):
                print('OIIIII')
                return "account not found", 404
            else:
                returnOperation = accounts[dataReceived['keyPix']].receivePix(dataReceived)
                if(returnOperation[0]==1):
                    dataSend = {
                        'idTransaction': returnOperation[1],
                        'mensage':"money received with sucess"
                    }
                    response = make_response(jsonify(dataSend))
                    return response, 200
                else:
                    dataSend = {
                        'idTransaction': returnOperation[1],
                        'mensage':"error in operation"
                    }
                    response = make_response(jsonify(dataSend))
                    return response, 400

        else:
            return 'not authorized', 401


"""
essa função asera usada para quando o cliente acessar de outro banco e quiser mandar um dinheiro que esta nesse
"""
@app.route('/account/send-pix', methods=['POST'])
def sendMoneyWithPix():
    dataReceived = request.json
    #adicionar a validação se esta autorizado ou nao para realizar aquilo
    if(dataReceived['authorization']):
        if(dataReceived['cpfCNPJSender'] not in accounts):
            return 'account not found', 404
        else:
            #ESSA RESPOSTA NAO PODE SER SIMPLISMENTE ESSA, TEM QUE MANDAR UM JSON COM AS INFOS DAS TRANSAÇÕES E SEUS IDs
            response = accounts[dataReceived['cpfCNPJSender']].sendPix(dataReceived['url'], dataReceived)
            dataSend = {
                'idTransactionSender': response[2],
                'idTransactionReceiver': response[3]
            }
            print('JSON ENVIADO: ', dataSend)
            response = make_response(jsonify(dataSend))
            return response, 200
    else:
        return 'not authorized', 401


@app.route('/account/confirmation-operation', methods=['POST'])
def confirmationOperation():
    dataReceived = request.json
    if(dataReceived['authorization']):
        if(dataReceived['cpfCNPJ'] not in accounts):
            return 'account not found', 404
        else:
            accounts[dataReceived['cpfCNPJ']].concludedTransaction(dataReceived['idTransaction'])
            return "operation Confirmed", 200
    else:
        return 'not authorized', 401
    

@app.route('/account/error-transaction', methods=['POST'])
def errorOperation():
    dataReceived = request.json
    if(dataReceived['authorization']):
        if(dataReceived['cpfCNPJ'] not in accounts):
            return 'account not found', 404
        else:
            accounts[dataReceived['cpfCNPJ']].errorTransaction(dataReceived['idTransaction'])
            return "operation updated",200
    else:
        return 'not authorized', 401


tokenTimeOutSend = False
initiateCouter =  False

def passToken():
    global hasToken
    global hadToken
    global operationOccurring
    global initiateCouter
    global nextNode
    global tokenTimeOutSend
    global tokenID
    global canPasstokenID
    nodeResponse = False
    if (hasToken and not operationOccurring and canPasstokenID):
        nextNode = int(selfID) + 1
        while not nodeResponse:
            if(str(nextNode) == selfID):
                nextNode = int(nextNode) +1
            if(int(nextNode) > 5):
                nextNode = 1
            if(str(nextNode) == selfID):
                nextNode = int(nextNode) +1
            dataSend={
                "nodeSender": selfID,
                "tokenIDList": tokenID
            }
            print('TOKEN QUE ESTOU ENVIANDO: ', tokenID)
            print("node da tentativa -> ",nextNode)
            nextNode = str(nextNode)
            url = f"{listBanksConsortium[nextNode][0]}/token"
            print(url)
            try:
                if(not operationOccurring):
                    infoReceived = requests.post(url=url, json=dataSend, timeout=1)
                    if(infoReceived.status_code == 200):
                        hasToken = False                #nao tem mais o token
                        operationOccurring = False      #nao tem operação acontecendo
                        nodeResponse = True             #sair do while indicando que conseguiu mandar o token
                        initiateCouter = True           #para iniciar o contador de que receber o token de novo
                        canPasstokenID = False
                        print('eu estava c o token')
                    elif(infoReceived.status_code == 405):
                        hasToken = False
                        operationOccurring = False      #nao tem operação acontecendo
                        nodeResponse = True             #sair do while indicando que conseguiu mandar o token
                        initiateCouter = True           #para iniciar o contador de que receber o token de novo
                        canPasstokenID = False
                        #error em passar isso
                        tokenID[int(selfID)-1] = 0
                        pass
                else:
                    pass
                
            except:
                print(f"node caiu -> {nextNode}")
                nextNode = int(nextNode)
                nextNode +=1


def passToken2():
    global hasToken
    global hadToken
    global operationOccurring
    global initiateCouter
    global nextNode
    global tokenTimeOutSend
    global tokenID
    global canPasstokenID
    nodeResponse = False
    nextNode = int(selfID) + 1
    while not nodeResponse:
        if(str(nextNode) == selfID):
            nextNode = int(nextNode) +1
        if(int(nextNode) > 5):
            nextNode = 1
        if(str(nextNode) == selfID):
            nextNode = int(nextNode) +1
        dataSend={
            "nodeSender": selfID,
            "tokenIDList": tokenID
        }
        print('TOKEN QUE ESTOU ENVIANDO: ', tokenID)
        print("node da tentativa -> ",nextNode)
        nextNode = str(nextNode)
        url = f"{listBanksConsortium[nextNode][0]}/token"
        
        try:
            hasToken = False                
            infoReceived = requests.post(url=url, json=dataSend, timeout=2)
            if(infoReceived.status_code == 200):
                nodeResponse = True             #sair do while indicando que conseguiu mandar o token
                initiateCouter = True           #para iniciar o contador de que receber o token de novo
            elif(infoReceived.status_code == 405):
                hasToken = False
                nodeResponse = True             #sair do while indicando que conseguiu mandar o token
                initiateCouter = True           #para iniciar o contador de que receber o token de novo
                #error em passar isso
                tokenID[int(selfID)-1] = 0
                pass
            else:
                pass
            
        except Exception as e:
            print('ERROR: ', e)
            print(f"node caiu -> {nextNode}")
            nextNode = int(nextNode)
            nextNode +=1


tokenTimeOut = False

requestPreviusNode = False
#fica sempre verificando se tem o token e nenhuma operação esta ocorrendo
#para se esse caso acontecer ele pegar e mandar o token p frente
def waitReceiveToken():
    global hasToken
    while True:
        if(hasToken):
            idToOperate  = selectTransactionToOperate()
            if(idToOperate[0]):
                print(idToOperate)
                operateTransactionOfList(idToOperate[1])
            passToken2()



'''
Esta função serve para realizar a contagem de tempo de quando ele deve receber o token novamente
se ele nao recebeu o token naquele tempo, entao ele pega e coloca outro token na rede
A contagem so inicia a partir do momento em que ele envia o token
'''
def timeOutReceiveToken():
    global initiateCouter
    global hasToken
    global counter 
    counter = 0
    attempts = 0
    timeToWait = 30 + (int(selfID)**2)**2
    while True:
        if(initiateCouter):
            for a in range(timeToWait):
                sleep(1)
                counter +=1
                print('VALOR DO CONTADOR: ', counter)
                '''
                verificação para o caso em que ele esta contando, e no meio ele recebeu o token
                1. ele reinicia a variavel contadora de tempo que esta sem receber conexão
                2. ele reinicia a variavel contadora de tentativas de conexão com o host anterior
                3. ele faz um break para sair do for
                '''
                if(not initiateCouter):
                    counter = 0
                    attempts = 0
                    break
            print('VALOR DO CONTADOR AO SAIR DO LOOP: ', counter)
            '''
            verificação para a contagem de tempo sem chegar o token
            1. verifica se bateu o tempo definido
            2. chama a função que verifica se o host que lhe enviou o token esta ativo
                2.1 se o host estiver ativo ele:
                    2.1.1 zera o contador de tempo
                    2.1.2 adiciona 1 na contagem de tentativas de comunicação com o anterior
                    2.1.3 mantem a variavel que deixa o contador ativo, como True
                    2.1.4 se houve 3 tentativas de conexão com o host anterior
                        2.1.4.1 vai colocar o token na rede de novo, ja que o anterior esta com problemas
                2.2 se o host nao estiver ativo ele:
                    2.2.1 fica com o token
                    2.2.2 zera o contado de tempo
                    2.2.3 indica para parar de contar o contador
                    2.2.4 ele vai nesse caso, o sistema, iniciar o processo como se tivesse recebido o token
                        2.2.4.1 vai verificar se tem alguma operação para realizar, se tiver realiza e depois passa o token
            '''
            if(counter >= timeToWait):
                if(conectBeforeHostTest()):
                    counter = 0
                    attempts +=1
                    initiateCouter = True
                    if(attempts == 3): #melhorar isso aq para poder enviar para todos que o novo token vai ta na rede
                        hasToken = True
                        attempts = 0
                        counter = 0
                        initiateCouter = False
                else:
                    hasToken = True
                    counter = 0
                    initiateCouter = False
        else:
            counter = 0
            attempts = 0


"""
Função para tentar se comunicar com o node anterior, se nao conseguir fica definitivo que caiu e entao coloca
outro token na rede para seguir o fluxo
"""
def conectBeforeHostTest():
    url = f"{listBanksConsortium[str(previousNode)][0]}/verify-conection"
    try:
        infoReceived = requests.get(url=url, timeout=5)
        if(infoReceived.status_code == 200):
            return 1 #nesse caso, o host ta ativo, entao reinicia a contagem
        else:
            #error em passar isso
            return 0
    except:
        #se entrou aq é pq nao conseguiu contato com o host anterior, e entao realmente vai ter que colocar o token de novo na rede
        return 0 #nesse caso, vai colocar o token na rede de novo, pq o anterior caiu

'''
função inativada
'''
def makeTransactionsOfTheList():
    global transactionsToMake
    global operationOccurring
    global transactionsToMakeID
    global hasToken
    global canPasstokenID
    while True:
        transactions = transactionsToMake.copy()
        if hasToken:
            
            if(len(transactionsToMake)>0):
                #print('TEM TRANSAÇÕES PARA EXECUTAR MEU\n', transactions)
                for transaction in transactions:
                    
                    if(transactions[transaction]["executed"] == False):
                        operationOccurring = True
                        canPasstokenID = False
                        operation = transactions[transaction]["operation"]
                        print('TRANSACTION A SER OPERADA: ', transactions[transaction]['operation']['operation'])
                        print("OPERARTION",operation)
                        if(operation["operation"] == 'create'):
                            if(operation["dataOperation"]["cpfCNPJ1"] in accounts):
                                addOperationLock.acquire()
                                transactionsToMake[transaction]["response"] = ('cpf already in system',405)
                                transactionsToMake[transaction]["executed"] = True
                                addOperationLock.release()
                                
                                operationOccurring = False
                                
                                
                            else:
                                banksList=[]
                                (banksList, hostNotResponse) = searchUserInOtherBanks(selfID, operation["dataOperation"]["cpfCNPJ1"])
                                banksList.append(listBanksConsortium[selfID][1])
                                accounts[operation["dataOperation"]["cpfCNPJ1"]] = createAccountObject(operation["dataOperation"],selfID, banksList) 
                                addOperationLock.acquire()
                                transactionsToMake[transaction]["response"] = (accounts[operation["dataOperation"]["cpfCNPJ1"]].jsonComplet(), 200)
                                transactionsToMake[transaction]["executed"] = True
                                addOperationLock.release()
                                
                                operationOccurring = False
                                canPasstokenID = True
                            break

                        elif(operation["operation"] == 'deposit'):
                            print('AAAAAAAAAAAAAAAAA')
                            if(operation['clientCpfCNPJ'] in accounts):
                                print('OLHA EU AQUI')
                                addOperationLock.acquire()
                                responseAboutOperation =accounts[operation['clientCpfCNPJ']].receiveDeposit(operation["dataOperation"]["value"])  
                                if(responseAboutOperation):
                                    transactionsToMake[transaction]["response"] = ("Money added with success", 200)
                                    transactionsToMake[transaction]["executed"] = True
                                    sleep(0.5)
                                    operationOccurring = False
                                else:
                                    transactionsToMake[transaction]["response"] = ("Error in adding money", 403)
                                    transactionsToMake[transaction]["executed"] = True
                                    sleep(0.5)
                                    operationOccurring = False
                                    canPasstokenID = True
                                addOperationLock.release()
                                
                            else:
                                transactionsToMake[transaction]["response"] = ("Account not found", 404)
                                transactionsToMake[transaction]["executed"] = True
                                operationOccurring = False
                                canPasstokenID = True
                            break
                        elif(operation["operation"]=="sendPix"):
                            addOperationLock.acquire()
                            if(operation['clientCpfCNPJ'] in accounts):
                                #enviar requisição para outro banco dizendo que quer fazer o pix
                                #tem que mandar para o outro banco um request autorizado 
                                    #para poder realizar a operação sem estar com o token
                                dataSend = {
                                    'authorization': hasToken,
                                    'nameSender': accounts[operation['clientCpfCNPJ']].name1,
                                    'cpfCNPJSender': operation['clientCpfCNPJ'],
                                    'value': operation["dataOperation"]["value"],
                                    'bankSourceName': listBanksConsortium[selfID][1],
                                    'keyPix': operation["dataOperation"]["keyPix"],
                                    'nameReceiver': operation["dataOperation"]["nameReceiver"],
                                    'bankNameReceiver': operation["dataOperation"]["bankNameReceiver"]
                                }
                                url = str(listBanksConsortium[str(operation["dataOperation"]["idBank"])][0])+'/account/receive-pix'
                                print(url)
                                response = accounts[operation['clientCpfCNPJ']].sendPix(url, dataSend)
                                if(response[1]==200):
                                    accounts[operation['clientCpfCNPJ']].concludedTransaction(response[2])
                                    dataSend = {
                                        'cpfCNPJ': operation["dataOperation"]["keyPix"],
                                        'idTransaction':response[3],
                                        'authorization': hasToken
                                    }
                                    url = str(listBanksConsortium[str(operation["dataOperation"]["idBank"])][0])+'/account/confirmation-operation'
                                    ok =False
                                    while not ok:
                                        try:
                                            infoReceivedByRequest = requests.post(url, json = dataSend)
                                            if(infoReceivedByRequest.status_code == 200):
                                                ok = True
                                        except:
                                            sleep(1)
                                            ok = False
                                transactionsToMake[transaction]["response"] = (response[0], response[1])
                                transactionsToMake[transaction]["executed"] = True
                                sleep(0.5)
                                operationOccurring = False
                                canPasstokenID = True
                            
                            addOperationLock.release()
                            break
                                #realiza primeiro a operação nessa conta que esta aqui
                                    #tem que mandar os devidos dados, ai vai precisar que a interface mande tb
                                #receber no retorno 
                                    #id da transação para depois mandar p aquele banco colocar como confirmado
                        elif(operation["operation"]=="packetPix"):
                            if(operation['clientCpfCNPJ'] in accounts):
                                packetTransactions = operation['dataOperation']
                                listConfirmation = 0
                                transactionsMade =0
                                for transaction in packetTransactions:
                                    print(transaction)
                                    idBankSender = ''
                                    if(transaction['bankSourceMoney'] == 'Eleven'):
                                        idBankSender = '1'
                                    elif(transaction['bankSourceMoney'] == 'Automobili'):
                                        idBankSender = '2'
                                    elif(transaction['bankSourceMoney'] == 'Secret'):
                                        idBankSender = '3'
                                    elif(transaction['bankSourceMoney'] == 'Formula'):
                                        idBankSender = '4'
                                    elif(transaction['bankSourceMoney'] == 'Titanium'):
                                        idBankSender = '5'

                                    dataSend = {
                                        'authorization': hasToken,
                                        'nameSender': accounts[operation['clientCpfCNPJ']].name1,
                                        'cpfCNPJSender': operation['clientCpfCNPJ'],
                                        'value': transaction['value'],
                                        'keyPix': transaction['keyPix'],
                                        'nameReceiver': transaction['nameReceiver'],
                                        'bankSourceName': transaction['bankSourceMoney'],
                                        'idBank': transaction['idBank'],
                                        'bankNameReceiver': listBanksConsortium[transaction['idBank']][1],
                                        'url': str(listBanksConsortium[transaction['idBank']][0])+'/account/receive-pix'
                                    }



                                    try:
                                        url = str(listBanksConsortium[idBankSender][0])+'/account/send-pix'
                                        infoReceived = requests.post(url,json=dataSend)
                                        if(infoReceived.status_code == 200):
                                            listConfirmation +=1
                                        else:
                                            break #colocar a logica para fazer depois do for
                                    except:
                                        break #colocar a logica para fazer depois do for

                            break   
                else:
                    canPasstokenID = True
            else:
                canPasstokenID = True



def operateTransactionOfList(idTransaction):
    global transactionsToMake
    global transactionsToMakeID
    transaction = transactionsToMake[idTransaction]
    addOperationLock.acquire()
    operation = transaction['operation']
    if(operation["operation"] == 'create'):
        if(operation["dataOperation"]["cpfCNPJ1"] in accounts):
            transactionsToMake[idTransaction]["response"] = ('cpf already in system',405)
            transactionsToMake[idTransaction]["executed"] = True    
        else:
            banksList=[]
            hostNotResponse = []
            (banksList, hostNotResponse) = searchUserInOtherBanks(selfID, operation["dataOperation"]["cpfCNPJ1"])
            banksList.append(listBanksConsortium[selfID][1])
            accounts[operation["dataOperation"]["cpfCNPJ1"]] = createAccountObject(operation["dataOperation"],selfID, banksList) 
            
            if(len(hostNotResponse)>0):
                data = {
                    'operation': 'completBanksListClient',
                    'clientCpfCNPJ': operation["dataOperation"]["cpfCNPJ1"],
                    'dataOperation': {
                        'banksNotResponse': hostNotResponse
                    }
                }
                transactionsToMake[transactionsToMakeID] = {
                                                'operation': data,
                                                'response': None,
                                                'executed': False
                                            }
                transactionsToMakeID +=1
            transactionsToMake[idTransaction]["response"] = (accounts[operation["dataOperation"]["cpfCNPJ1"]].jsonComplet(), 200)
            transactionsToMake[idTransaction]["executed"] = True
    elif(operation["operation"] == 'completBanksListClient'):
        listToSearch = operation['dataOperation']['banksNotResponse']
        banksList = []
        hostNotResponse = []
        (banksList, hostNotResponse) = searchUserInOtherBanks(selfID, operation["clientCpfCNPJ"])
        for bank in banksList:
            accounts[operation["clientCpfCNPJ"]].addBankToList(bank)
        if(len(hostNotResponse)>0):
            data = {
                'operation': 'completBanksListClient',
                'clientCpfCNPJ': operation["clientCpfCNPJ"],
                'dataOperation': {
                    'banksNotResponse': hostNotResponse
                }
            }
            transactionsToMake[transactionsToMakeID] = {
                                            'operation': data,
                                            'response': None,
                                            'executed': False
                                        }
            transactionsToMakeID +=1
        else:
            transactionsToMake[idTransaction]["response"] = ('Search in all banks complete', 200)
            transactionsToMake[idTransaction]["executed"] = True
        
    #essa operação de deposit vai acontecer e nao depende dos outros hosts para poder operar
    #sendo assim ela pode ser concluida mesmo quando a conexão é perdida
    elif(operation["operation"] == 'deposit'):
        if(operation['clientCpfCNPJ'] in accounts):
            responseAboutOperation =accounts[operation['clientCpfCNPJ']].receiveDeposit(operation["dataOperation"]["value"])  
            if(responseAboutOperation):
                transactionsToMake[idTransaction]["response"] = ("Money added with success", 200)
                transactionsToMake[idTransaction]["executed"] = True

            else:
                transactionsToMake[idTransaction]["response"] = ("Error in adding money", 403)
                transactionsToMake[idTransaction]["executed"] = True
        else:
            transactionsToMake[idTransaction]["response"] = ("Account not found", 404)
            transactionsToMake[idTransaction]["executed"] = True
    elif(operation["operation"]=="sendPix"):
        if(operation['clientCpfCNPJ'] not in accounts):
            transactionsToMake[idTransaction]["response"] = ("Account not found", 404)
            transactionsToMake[idTransaction]["executed"] = True
        if(operation['clientCpfCNPJ'] in accounts):
            #enviar requisição para outro banco dizendo que quer fazer o pix
            #tem que mandar para o outro banco um request autorizado 
                #para poder realizar a operação sem estar com o token
            dataSend = {
                'authorization': hasToken,
                'nameSender': accounts[operation['clientCpfCNPJ']].name1,
                'cpfCNPJSender': operation['clientCpfCNPJ'],
                'value': operation["dataOperation"]["value"],
                'bankSourceName': listBanksConsortium[selfID][1],
                'keyPix': operation["dataOperation"]["keyPix"],
                'nameReceiver': operation["dataOperation"]["nameReceiver"],
                'bankNameReceiver': operation["dataOperation"]["bankNameReceiver"]
            }
            url = str(listBanksConsortium[str(operation["dataOperation"]["idBank"])][0])+'/account/receive-pix'
            response = accounts[operation['clientCpfCNPJ']].sendPix(url, dataSend)
            if(response[1]==200):
                
                dataSend = {
                    'cpfCNPJ': operation["dataOperation"]["keyPix"],
                    'idTransaction':response[3],
                    'authorization': hasToken
                }
                url = str(listBanksConsortium[str(operation["dataOperation"]["idBank"])][0])+'/account/confirmation-operation'
                ok =False
                while not ok:
                    try:
                        infoReceivedByRequest = requests.post(url, json = dataSend)
                        if(infoReceivedByRequest.status_code == 200):
                            ok = True
                            accounts[operation['clientCpfCNPJ']].concludedTransaction(response[2])
                    except:
                        sleep(1)
                        ok = False
            
            transactionsToMake[idTransaction]["response"] = (response[0], response[1])
            transactionsToMake[idTransaction]["executed"] = True
    elif(operation["operation"]=="packetPix"):
        if(operation['clientCpfCNPJ'] in accounts):
            packetTransactions = operation['dataOperation']
            listConfirmation = 0
            transactionsMadeInfo = []
            sendOK=True
            #PRIMEIRO FOR PARA ENVIAR O DINHEIRO
            for transaction in packetTransactions:
                print(transaction)
                if(sendOK):
                    #selecao do id de onde vai sair o dinheiro
                    idBankSender = ''
                    if(transaction['bankSourceMoney'] == 'Eleven'):
                        idBankSender = '1'
                    elif(transaction['bankSourceMoney'] == 'Automobili'):
                        idBankSender = '2'
                    elif(transaction['bankSourceMoney'] == 'Secret'):
                        idBankSender = '3'
                    elif(transaction['bankSourceMoney'] == 'Formula'):
                        idBankSender = '4'
                    elif(transaction['bankSourceMoney'] == 'Titanium'):
                        idBankSender = '5'

                    #montagem dos dados que o outro banco vai precisar para executar a operação
                    dataSend = {
                        'authorization': hasToken,
                        'nameSender': accounts[operation['clientCpfCNPJ']].name1,
                        'cpfCNPJSender': operation['clientCpfCNPJ'],
                        'value': transaction['value'],
                        'keyPix': transaction['keyPix'],
                        'nameReceiver': transaction['nameReceiver'],
                        'bankSourceName': transaction['bankSourceMoney'],
                        'idBank': transaction['idBank'],
                        'bankNameReceiver': listBanksConsortium[transaction['idBank']][1],
                        'url': str(listBanksConsortium[transaction['idBank']][0])+'/account/receive-pix'
                    }


                    #tenta mandar para o banco que vai sair o dinheiro
                    try:
                        url = str(listBanksConsortium[idBankSender][0])+'/account/send-pix'
                        infoReceived = requests.post(url,json=dataSend)
                        print('passeando por ca')
                        if(infoReceived.status_code == 200):
                            listConfirmation +=1
                            print('mais interno')
                            print(infoReceived)
                            infoReceivedJson = infoReceived.json()
                            print(infoReceivedJson)
                            
                            print(transactionsMadeInfo)
                            transactionsMadeInfo.append(
                                {
                                    'idTransactionSender':infoReceivedJson['idTransactionSender'],
                                    'idTransactionReceiver':infoReceivedJson['idTransactionReceiver'],
                                    'idBankSender':idBankSender,
                                    'keyPix':transaction['keyPix'],
                                    'cpfCNPJSender':operation['clientCpfCNPJ'],
                                    'idBankReceiver':transaction['idBank']
                                }
                            )
                            # transactionsMadeInfo[transaction]['idTransactionSender'] = infoReceivedJson['idTransactionSender']
                            # transactionsMadeInfo[transaction]['idTransactionReceiver'] = infoReceivedJson['idTransactionReceiver']
                            # transactionsMadeInfo[transaction]['idBankSender'] = idBankSender
                            # transactionsMadeInfo[transaction]['idBankReceiver'] = transaction['idBank']
                            # transactionsMadeInfo[transaction]['keyPix'] =  transaction['keyPix']
                            # transactionsMadeInfo[transaction]['cpfCNPJSender'] =  operation['clientCpfCNPJ']
                            print(transactionsMadeInfo)
                        else:
                            sendOK = False
                            #colocar a logica para fazer depois do for
                    #se der erro nessa operação, ja nao vai operar mais 
                    except:
                        print('entrei bem aqui')
                        sendOK = False
            if(listConfirmation != len(packetTransactions)):
                print('para para para')
                #SEGUNDO FOR PARA ENVIAR QUE DEU ERRADO PARA A GALERA
                for transaction in transactionsMadeInfo:
                    url = listBanksConsortium[transaction['idBankSender']][0]+'/account/error-transaction'
                    dataSend = {
                        'cpfCNPJ': transaction['cpfCNPJSender'],
                        'idTransaction': transaction['idTransactionSender'],
                        'authorization': hasToken
                    }
                    ok = False
                    while not ok:
                        try:
                            infoReceivedByRequest = requests.post(url, json = dataSend)
                            if(infoReceivedByRequest.status_code == 200):
                                ok = True
                        except:
                            sleep(1)
                            ok = False
                    url = listBanksConsortium[transaction['idBankReceiver']][0]+'/account/error-transaction'
                    dataSend = {
                        'cpfCNPJ': transaction['keyPix'],
                        'idTransaction': transaction['idTransactionReceiver'],
                        'authorization': hasToken
                    }
                    ok = False
                    while not ok:
                        try:
                            infoReceivedByRequest = requests.post(url, json = dataSend)
                            if(infoReceivedByRequest.status_code == 200):
                                ok = True
                        except:
                            sleep(1)
                            ok = False
                transactionsToMake[idTransaction]["response"] = ('one, or more, transaction(s) not ok', 400)
                transactionsToMake[idTransaction]["executed"] = True  
            
            
            elif(listConfirmation == len(packetTransactions)):
                print('oieee')
                print(transactionsMadeInfo)
                #SEGUNDO FOR PARA ENVIAR A TODOS A CONFIRMAÇÃO DA OPERAÇÃO
                for transaction in transactionsMadeInfo:
                    print('transaction')
                    print(transaction)
                    print('id do banco')
                    print(transaction['idBankSender'])
                    print('acessando dicio')
                    print(transaction)
                    url = listBanksConsortium[transaction['idBankSender']][0]+'/account/confirmation-operation'
                    dataSend = {
                        'cpfCNPJ': transaction['cpfCNPJSender'],
                        'idTransaction': transaction['idTransactionSender'],
                        'authorization': hasToken
                    }
                    ok = False
                    while not ok:
                        try:
                            infoReceivedByRequest = requests.post(url, json = dataSend)
                            if(infoReceivedByRequest.status_code == 200):
                                ok = True
                        except:
                            sleep(1)
                            ok = False
                    url = listBanksConsortium[transaction['idBankReceiver']][0]+'/account/confirmation-operation'
                    dataSend = {
                        'cpfCNPJ': transaction['keyPix'],
                        'idTransaction': transaction['idTransactionReceiver'],
                        'authorization': hasToken
                    }
                    ok = False
                    while not ok:
                        try:
                            infoReceivedByRequest = requests.post(url, json = dataSend)
                            if(infoReceivedByRequest.status_code == 200):
                                ok = True
                        except:
                            sleep(1)
                            ok = False
                transactionsToMake[idTransaction]["response"] = ('transactions made are ok', 200)
                transactionsToMake[idTransaction]["executed"] = True

    addOperationLock.release()


def selectTransactionToOperate():
    global transactionsToMake
    transactions = transactionsToMake.copy()
    for transaction in transactions:
        if(transactions[transaction]["executed"] == False):
            print(transaction)
            return (True, transaction)
    else:
        return (False, None)

def searchUserInOtherBanks(selfID, cpfCNPJ1):
    nextNode = int(selfID) + 1
    nodeIniciated = nextNode
    nodeResponse = False
    banksList = []
    hostNotResponse= []
    while not nodeResponse:
        print(nextNode)
        print(selfID)
        if(int(nextNode) > 5):
            nextNode = 1
        if(str(nextNode) == str(selfID)):
            break
            print("ENTREI")
        nextNode = str(nextNode)
        url = f"{listBanksConsortium[nextNode][0]}/search-account"
        print(url)
        dataSend = {
            'cpfCNPJ1': cpfCNPJ1,
            'bankName': listBanksConsortium[str(selfID)][1] 
        }
        try:
            infoReceived = requests.post(url=url, json=dataSend, timeout=1)
            if(infoReceived.status_code == 200):
                banksList.append(listBanksConsortium[nextNode][1])
                nextNode = int(nextNode)
                nextNode +=1
            elif(infoReceived.status_code == 404):
                nextNode = int(nextNode)
                nextNode +=1
        except:
            hostNotResponse.append(nextNode)
            nextNode = int(nextNode)
            nextNode +=1
    return (banksList, hostNotResponse)


def putOperationInList(dataReceived):
    global transactionsToMake
    global operationOccurring
    global transactionsToMakeID
    global hasToken
    transactionsToMakeIDWaiting = transactionsToMakeID
    addOperationLock.acquire()
    transactionsToMake[transactionsToMakeID] = {
        'operation': dataReceived,
        'response': None,
        'executed': False
    }
    transactionsToMakeID +=1
    addOperationLock.release()
    return transactionsToMakeIDWaiting



def createAccountObject(dataReceived, selfID, banksList):
    
    account = Account(
                name1= dataReceived["name1"],
                cpfCNPJ1= dataReceived["cpfCNPJ1"],
                name2= dataReceived["name2"],
                cpfCNPJ2= dataReceived["cpfCNPJ2"],
                email=dataReceived["email"],
                password= cryptographyPassword(dataReceived["password"]),
                isFisicAccount= dataReceived["isFisicAccount"],
                isJoinetAccount=dataReceived["isJoinetAccount"],
                accountNumber= accountNumbers.createAccountNumber(),
                telephone= dataReceived["telephone"],
                bank=listBanksConsortium[selfID][1],
                balance="0",
                blockedBalance="0",
                listBanks=banksList,
                )
    print(account)
    return account


def cryptographyPassword(password):
    encryptedPassword = sha512(password.encode()).digest()
    return encryptedPassword

class GenerateNumberAccountBank:
    def __init__(self):
        self.accountNumbersInSystem = set()
    def createAccountNumber(self):
            while True:
                accountNumber = random.randint(1000, 9999)
                if accountNumber not in self.accountNumbersInSystem:
                    self.accountNumbersInSystem.add(accountNumber)
                    return accountNumber


global accountNumbers
accountNumbers = GenerateNumberAccountBank()







if(selfID == "1"):
    sleep(2)
    hasToken = True
    canPasstokenID = True

threading.Thread(target=waitReceiveToken, daemon=True).start()
threading.Thread(target=timeOutReceiveToken, daemon=True).start()
#threading.Thread(target=makeTransactionsOfTheList, daemon=True).start()

app.run(addressBank, portBank, debug=False, threaded=True)

