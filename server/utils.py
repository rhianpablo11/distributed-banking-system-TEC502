from hashlib import sha512
import random
import uuid
import requests
import threading
import os
from pathlib import Path
from accountModel import Account





global listBanksConsortium
listBanksConsortium = {
    "1": "http://localhost:8081",
    "2": "http://localhost:8082",
    "3": "http://localhost:8083",
    "4": "http://localhost:8084",
    "5": "http://localhost:8085"
}

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








def createAccountObject(dataReceived, selfID, bankName):
    
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
                                bank=bankName,
                                balance="0",
                                blockedBalance="0",
                                listBanks=dataReceived["listBanks"],
                                )
    return account

