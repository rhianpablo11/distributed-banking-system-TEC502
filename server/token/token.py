global has_token
global counter_token
counter_token = []
has_token = False

def get_if_has_token():
    return has_token

def set_has_token(token):
    global has_token
    has_token = token


def pass_token():
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