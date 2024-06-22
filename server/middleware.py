global listBanksConsortium
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
accounts = {}

accountsLock = threading.Lock()


listBanksConsortium = {
    "1": ["http://localhost:8081", "Eleven Bank"],
    "2": ["http://localhost:8082", "Automobili Bank"],
    "3": ["http://localhost:8083", "Secret Bank"],
    "4": ["http://localhost:8084", "Formula Bank"],
    "5": ["http://localhost:8085", "Titanium Bank"]
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
global hadToken
global operationOccurring
global previousNode
global nextNode

hasToken = False
hadToken = False
operationOccurring =  False

@app.route('/account/create', methods=['POST'])
def createaccount():
    global accounts
    dataReceived = request.json
    
    #verificar se tem todos os elementos
    infosComplet =True
    
    if(infosComplet):
        if(dataReceived["cpfCNPJ1"] in accounts):
            return "user already in system", 409
        else:
            clientExists = searchClient(dataReceived["cpfCNPJ1"], selfID) #nao pode requisitar para o mesmo banco
            if(clientExists[0]):
                #o cliente existe
                
                pass
            else: #o cliente nao existe
                accounts[dataReceived["cpfCNPJ1"]]  = createAccountObject(dataReceived, selfID, listBanksConsortium[selfID][1])
                
                return accounts[dataReceived["cpfCNPJ1"]].jsonComplet(), 201
                
            
    else:
        
        return "infos received not are complete", 406


        
@app.route('/accounts', methods=['GET'])
def getaccountsList():
    accountsList = []
    if(len(accounts) >0):
        for account in accounts:
            accountsList.append(accounts[account].jsonComplet())
    response = make_response(jsonify(accountsList))
    
    return response



@app.route('/token', methods=['POST'])
def receiveToken():
    global hasToken
    global hadToken
    global operationOccurring
    global previousNode
    hasToken = True
    hadToken = False
    infoReceived = request.json
    previousNode = infoReceived["nodeSender"]
    sleep(2)
    print("peguei o token")
    #vai pegar e passar para o proximo da fila
    return "ok", 200

@app.route("/token-backup", methods=['POST'])
def tokenBackupWithMe():
    global hasToken
    global hadToken
    if(hasToken):
        return "token with me", 200
    else:
        return "not token with me", 406

@app.route('/token-delete-backup', methods=['DELETE'])
def tokenBackupDelete():
    global hasToken
    global hadToken
    hasToken = False                #nao tem mais o token
    hadToken = False                #backup do token
    print("Token backup has deleted")
    return "deleted with success",200

global timeOutTokenCounter
global initiateCouter
global tokenTimeOutSend
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
            if(nextNode > 5):
                nextNode = 1
            if(str(nextNode) == selfID):
                nextNode = int(nextNode) +1
            dataSend={
                "nodeSender": selfID
            }
            print("node da tentativa -> ",nextNode)
            nextNode = str(nextNode)
            url = f"{listBanksConsortium[nextNode][0]}/token"
            # envolver em um while, q sai daqui quando terminar confirmar que enviou
            try:
                sleep(20)
                infoReceived = requests.post(url=url, json=dataSend)
                if(infoReceived.status_code == 200):
                    hasToken = False                #nao tem mais o token
                    operationOccurring = False      #nao tem operação acontecendo
                    hadToken = True                 #backup do token
                    initiateCouter = True           #inicia contagem para o timeout de passar o token por ele denovo
                    nodeResponse = True             #sair do while indicando que conseguiu mandar o token
                    print('eu estava c o token')
                    #colocar para passar para o no anterior do anterior que perdeu o backup do token
                    try:
                        url = f"{listBanksConsortium[str(previousNode)][0]}/token-delete-backup"
                        infoReceived = requests.delete(url=url)
                    except:
                        pass
                else:
                    #error em passar isso
                    pass
            except:
                print(f"node caiu -> {nextNode}")
                nextNode = int(nextNode)
                nextNode +=1


global tokenTimeOut
tokenTimeOut = False
global requestPreviusNode
requestPreviusNode = False
#fica sempre verificando se tem o token e nenhuma operação esta ocorrendo
#para se esse caso acontecer ele pegar e mandar o token p frente
def waitReceiveToken():
    global hasToken
    global hadToken
    global operationOccurring
    global initiateCouter
    while True:
        if(hasToken and not operationOccurring and not tokenTimeOut):
            passToken()
            initiateCouter = False
        elif(tokenTimeOut):
            # chama a função que vai mandar para o node anterior ao que deveria
            # ter mandando para ca
            requestPreviousNodeForToken()
            pass
        elif(tokenTimeOutSend):
            hadToken = False
            hasToken = False
            initiateCouter = False



#fica contando depois que recebeu uma mensagem para ver se ja passou o tempo de receber algo de novo
def activeTimeOutToken():
    global tokenTimeOut
    timeOutTokenCounter =0
    global initiateCouter
    while True:
        if(initiateCouter):
            for a in range(30):
                if(initiateCouter):
                    timeOutTokenCounter +=1
                    sleep(1)
                    print(f"temporizador out: {timeOutTokenCounter}")
                else:
                    print("breakout contagem: ", initiateCouter, hasToken, hadToken)
                    break
            if(timeOutTokenCounter == 30):
                tokenTimeOut = True
        else:
            timeOutTokenCounter =0
            tokenTimeOut = False
        

"""
se o node previous ja tiver recebido o ok de que ele tava com o token
e nao tiver mais o backup, esse cara daqui que detectou deve pegar e colocar o token novamente na rede
"""
def requestPreviousNodeForToken():
    global hasToken
    nodePrevious = int(selfID) - 2
    if(nodePrevious == 0):
        nodePrevious = 5
    elif(nodePrevious == -1):
        nodePrevious = 4
    
    url = f"{listBanksConsortium[str(nodePrevious)][0]}/token-backup"
    try:
        infoReceived = requests.post(url=url)
        if(infoReceived.status_code == 200):
            hasToken = True
            
        elif(infoReceived.status_code == 406):
            hasToken = True
            #error em passar isso
    except:
        print("node anterior caiu")


#faz a contagem de se ja passou o tempod                          
def activeTimeOutSendToken():
    
    global tokenTimeOutSend
    timeOutTokenCounter =0
    global initiateCouterSend

    while True:
        if(hadToken):
            for a in range(15):
                if(hadToken):
                    timeOutTokenCounter +=1
                    sleep(1)
                    print(f"temporizador send: {timeOutTokenCounter}")
                else:
                    break
            if(timeOutTokenCounter == 15):
                tokenTimeOutSend = True
        else:
            timeOutTokenCounter =0
            tokenTimeOutSend = False


if(selfID == "1"):
    hasToken = True

threading.Thread(target=waitReceiveToken, daemon=True).start()
threading.Thread(target=activeTimeOutToken, daemon=True).start()
threading.Thread(target=activeTimeOutSendToken, daemon=True).start()

app.run(addressBank, portBank, debug=False, threaded=True)

