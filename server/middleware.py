
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
transactionsToMake = []
disconnectionOcurred = False
tokenID = [0,0,0,0,0]

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


@app.route('/operations', methods=['POST'])
def putOperationInList():
    dataReceived = request.json
    global transactionsToMake
    transactionsToMake.append(dataReceived)
    return "ok", 200

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
        if(hasToken and not operationOccurring):
            
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
    global hasToken
    while True:
        transactions = transactionsToMake.copy()
        while hasToken:
            
            if(len(transactionsToMake)>0):
                operationOccurring = True
                print(transactionsToMake)
                for transaction in transactions:
                    print(transaction)
                    if(transaction["operation"] == 'create'):
                        if(transaction["dataOperation"]["cpfCNPJ1"] in accounts):
                            operationOccurring = False
                            return "cpf already in system", 405
                        else:
                            (banksList, hostNotResponse) = searchUserInOtherBanks(selfID, transaction["dataOperation"]["cpfCNPJ1"])
                            print(banksList)
                            accounts[transaction["dataOperation"]["cpfCNPJ1"]] = createAccountObject(transaction["dataOperation"],selfID, banksList)
                            print('TRABNSACTION ', transaction)
                            print('TRABNSACTIONS    ', transactionsToMake)
                            transactionsToMake.remove(transaction)
                            
                            
                            operationOccurring = False



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

