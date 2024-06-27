from hashlib import sha512
import random
import uuid
import requests
import threading
import os
from pathlib import Path
from accountModel import Account
from middleware import listBanksConsortium


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
            

'''
A ideia dessa classe é gerar um id em que ele é "externo", logo assim de conhecimento dos envolvidos,
dessa forma será possivel ao fim do pacote de transações, é enviado para os bancos que precisa validar as transações
que estavam pendentes, e quando isso acontecer, diz OK
'''
class GenerateIDTransaction:
    def __init__(self):
        self.HashIDGenerateds = set()
        self.IDBankSender = 0

    def generateID(self):
        id = str(uuid.uuid4())
        id = str(f"bankID={self.IDBankSender}?{id}")
        return id

global accountNumbers
accountNumbers = GenerateNumberAccountBank()


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

def searchUserInOtherBanks(selfID, cpfCNPJ1):
    nextNode = int(selfID) + 1
    nodeIniciated = nextNode
    nodeResponse = False
    banksList = []
    hostNotResponse= []
    while not nodeResponse:
        if(str(nextNode) == selfID):
            nodeResponse = True
        if(int(nextNode) > 5):
            nextNode = 1
        if(str(nextNode) == selfID):
            nextNode = int(nextNode) +1

        nextNode = str(nextNode)
        url = f"{listBanksConsortium[nextNode][0]}/search-account"
        print(url)
        dataSend = {
            'cpfCPNJ1': cpfCNPJ1,
            'bankName': listBanksConsortium[str(selfID)][1] 
        }
        try:
            infoReceived = requests.post(url=url, json=dataSend)
            if(infoReceived.status_code == 200):
                banksList.append(listBanksConsortium[nextNode][1])
                pass
            elif(infoReceived.status_code == 404):
                nextNode = int(nextNode)
                nextNode +=1
        except:
            hostNotResponse.append(nextNode)
            nextNode = int(nextNode)
            nextNode +=1
    return (banksList, hostNotResponse)