
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



argumento =sys.argv[1:]
print(argumento)
selfID=argumento[0]
if(argumento[0] == "1" or argumento[0] == "2" or argumento[0] == "3" or argumento[0] == "4" or argumento[0] == "5"):
        
    value = listBanksConsortium[argumento[0]][0]
    print(value)
    value=value.split(":")
    valueIP = ""
    valuePort = ""
    portBank = value[len(value)-1]


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
transactionsToMakeID = 0
transactionsToMake = {}
disconnectionOcurred = False
tokenID = [0,0,0,0,0]
addOperationLock = threading.Lock()
hasToken = False
hadToken = False
operationOccurring =  False
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
    
    infoReceived = request.json
    previousNode = infoReceived["nodeSender"]
    tokenIDNew = infoReceived["tokenIDList"]
    print(tokenIDNew)
    print(tokenID)
    print(tokenIDNew[int(selfID)-1])
    print(tokenID[int(selfID)-1])
    if(tokenIDNew[int(selfID)-1] == tokenID[int(selfID)-1]):
        tokenID = tokenIDNew 
        tokenID[int(selfID)-1] +=1
        hasToken = True
        print(tokenID)
        return "ok", 200
    else:
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
    addOperationLock.release()
    while (transactionsToMake[transactionsToMakeIDWaiting]["executed"]==False):
        pass   
    print(hasToken)
    print(operationOccurring)
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
    if(data["bankID"] == "1"):
        url = "http://"+hashMapBanks[data["bankID"]]+"/account/pix"
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



tokenTimeOutSend = False
initiateCouter =  False

def passToken():
    global hasToken
    global hadToken
    global operationOccurring
    global initiateCouter
    global nextNode
    global tokenTimeOutSend
    nodeResponse = False
    if (hasToken and not operationOccurring and not tokenTimeOutSend):
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
            print("node da tentativa -> ",nextNode)
            nextNode = str(nextNode)
            url = f"{listBanksConsortium[nextNode][0]}/token"
            print(url)
            try:
                infoReceived = requests.post(url=url, json=dataSend)
                if(infoReceived.status_code == 200):
                    hasToken = False                #nao tem mais o token
                    operationOccurring = False      #nao tem operação acontecendo
                    nodeResponse = True             #sair do while indicando que conseguiu mandar o token
                    initiateCouter = True           #para iniciar o contador de que receber o token de novo
                    print('eu estava c o token')
                elif(infoReceived.status_code == 405):
                    hasToken = False
                    operationOccurring = False      #nao tem operação acontecendo
                    nodeResponse = True             #sair do while indicando que conseguiu mandar o token
                    initiateCouter = True           #para iniciar o contador de que receber o token de novo
                    #error em passar isso
                    pass
            except:
                print(f"node caiu -> {nextNode}")
                nextNode = int(nextNode)
                nextNode +=1

tokenTimeOut = False

requestPreviusNode = False
#fica sempre verificando se tem o token e nenhuma operação esta ocorrendo
#para se esse caso acontecer ele pegar e mandar o token p frente
def waitReceiveToken():
    global hasToken
    global hadToken
    global operationOccurring
    global initiateCouter
    while True:
        if(hasToken):
            sleep(1)
            if(not operationOccurring):
                print('NO OPERATIOON OCURRING')
                passToken()
                initiateCouter = False


'''
Esta função serve para realizar a contagem de tempo de quando ele deve receber o token novamente
se ele nao recebeu o token naquele tempo, entao ele pega e coloca outro token na rede
A contagem so inicia a partir do momento em que ele envia o token
'''
def timeOutReceiveToken():
    global initiateCouter
    global hasToken
    counter = 0
    while True:
        if(initiateCouter):
            for a in range(50):
                sleep(1)
                counter +=1
            print(counter)
            if(counter == 50):
                if(conectBeforeHostTest()):
                    counter = 0
                    initiateCouter = True
                else:
                    hasToken = True
                    counter = 0
                    initiateCouter = False
                


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
            pass
    except:
        #se entrou aq é pq nao conseguiu contato com o host anterior, e entao realmente vai ter que colocar o token de novo na rede
        return 0 #nesse caso, vai colocar o token na rede de novo, pq o anterior caiu


def makeTransactionsOfTheList():
    global transactionsToMake
    global operationOccurring
    global transactionsToMakeID
    global hasToken
    while True:
        transactions = transactionsToMake.copy()
        if hasToken:
            if(len(transactionsToMake)>0):
                for transaction in transactions:
                    if(transactions[transaction]["executed"] == False):
                        operationOccurring = True
                        operation = transactions[transaction]["operation"]
                        transactionsToMakeID +=1
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

                        elif(operation["operation"] == 'deposit'):
                            if(operation['clientCpfCNPJ'] in accounts):
                                addOperationLock.acquire()
                                responseAboutOperation =accounts[operation['clientCpfCNPJ']].receiveDeposit(operation["dataOperation"]["value"])  
                                if(responseAboutOperation):
                                    transactionsToMake[transaction]["response"] = ("Money added with success", 200)
                                    transactionsToMake[transaction]["executed"] = True
                                    operationOccurring = False
                                else:
                                    transactionsToMake[transaction]["response"] = ("Error in adding money", 403)
                                    transactionsToMake[transaction]["executed"] = True
                                    operationOccurring = False
                                addOperationLock.release()
                        
                        elif(operation["operation"]=="sendPix"):
                            if(operation['clientCpfCNPJ'] in accounts):
                                #enviar requisição para outro banco dizendo que quer fazer o pix
                                #tem que mandar para o outro banco um request autorizado 
                                    #para poder realizar a operação sem estar com o token
                                
                                #realiza primeiro a operação nessa conta que esta aqui
                                    #tem que mandar os devidos dados, ai vai precisar que a interface mande tb
                                    

                                #mandar o seguinte conjunto de dados:
                                    #nome de quem da enviando
                                    #cpf de quem ta enviando
                                    #valor
                                    #bankSource Name

                                #receber no retorno 
                                    #id da transação para depois mandar p aquele banco colocar como confirmado



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
            infoReceived = requests.post(url=url, json=dataSend)
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
    hasToken = True

threading.Thread(target=waitReceiveToken, daemon=True).start()
threading.Thread(target=timeOutReceiveToken, daemon=True).start()
threading.Thread(target=makeTransactionsOfTheList, daemon=True).start()

app.run(addressBank, portBank, debug=False, threaded=True)

