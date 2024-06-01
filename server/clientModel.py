import threading
from transactionModel import Transaction
from datetime import *
import requests

class Client:
    def __init__(self, name1, name2, cpfCNPJ1, cpfCNPJ2, email, password, isFisicAccount, accountNumber, telephone, bank, isJoinetAccount, balance, blockedBalance):
        self.email = email
        self.password = password
        self.isJoinetAccount = isJoinetAccount
        self.isFisicAccount = isFisicAccount
        self.id = hash(cpfCNPJ1)
        self.keyPix = None
        self.accountNumber = accountNumber
        self.telephone = telephone
        self.bank = bank
        self.balance = balance
        self.blockedBalance = blockedBalance
        self.transactions = {}
        self.idLastTransaction = 0
        self.operationLock = threading.Lock()
        if(isJoinetAccount):
            self.name1 = name1
            self.cpfCNPJ1 = cpfCNPJ1
            self.name2 = name2
            self.cpfCNPJ2 = cpfCNPJ2
        else:
            self.name1 = name1
            self.cpfCNPJ1 = cpfCNPJ1
    

    def jsonComplet(self):
        self.operationLock.acquire()
        auxJson = {
            "telephone": self.telephone,
            "email": self.email,
            "accountNumber": self.accountNumber,
            "keyPix": self.keyPix,
            "isFisicAccount": self.isFisicAccount,
            "bank": self.bank,
            "balance": str(self.balance),
            "blockedBalance": self.blockedBalance
        }
        listTransactions = []
        for transaction in self.transactions:
            listTransactions.append(self.transactions[transaction].getJsonTransaction())

        auxJson["transactions"] = listTransactions

        if(self.isJoinetAccount=="True"):
            auxJson["isJoinet"] = "True"
            auxJson["cpfCNPJ1"] = self.cpfCNPJ1
            auxJson["cpfCNPJ2"] = self.cpfCNPJ2
            auxJson["name1"] = self.name1
            auxJson["name2"] = self.name2
        else:
            auxJson["isJoinet"] = "False"
            auxJson["cpfCNPJ1"] = self.cpfCNPJ1
            auxJson["name1"] = self.name1
        
        self.operationLock.release()
        return auxJson
    

    def infoBasic(self): #verificar se a chave nao é a do mesmo usuario
        self.operationLock.acquire()
        print("Thread info basic",threading.current_thread())
        print(datetime.now())
        auxJson = {}
        auxJson["bank"] = self.bank
        if(self.isJoinetAccount):
            auxJson["name"] = self.name1
            cpfCamufled = "***."+self.cpfCNPJ1[4:8]+"***"+self.cpfCNPJ1[11:14]
            auxJson["cpfCNPJ1"] = cpfCamufled
        else:
            auxJson["name"] = self.name
            cpfCamufled = "***."+self.cpfCNPJ1[4:8]+"***"+self.cpfCNPJ1[11:14]
            auxJson["cpfCNPJ1"] = cpfCamufled
        self.operationLock.release()
        return auxJson
        

    def setKeyPix(self, active):
        self.operationLock.acquire()
        if(active == "True"):
            self.keyPix = self.cpfCNPJ1
        else:
            self.keyPix = None
        self.operationLock.release()


    def setBalance(self, newBalance):
        self.operationLock.acquire()
        self.balance = newBalance
        self.operationLock.release()


    def setBlockedBalance(self, blockedValue):
        oldBlocked = float(self.blockedBalance)
        oldBlocked += blockedValue
        self.blockedBalance = oldBlocked


    def addTransaction(self, transaction):
        self.idLastTransaction = transaction.idTransaction
        self.transactions[transaction.idTransaction] = transaction


    def receiveDeposit(self, value):
        self.operationLock.acquire()
        print("operation lock pegado ", self.operationLock)
        print("Thread deposit",threading.current_thread())
        print(datetime.now())
        self.balance = float(self.balance) + float(value) 
        self.addTransaction(
            Transaction(
                        source="none",
                        receptor=self.name1,
                        value=value,
                        dateTransaction= datetime.now(),
                        concluded=True,
                        typeTransaction="deposit",
                        idTransaction=self.idLastTransaction + 1,
                        bankReceptor=self.bank,
                        bankSource=self.bank
                    )
        )
        self.operationLock.release()
        print("operation lock pegado ", self.operationLock)
        return 1


    def receivePix(self, value, bankSourceName, source):
        self.operationLock.acquire()
        self.balance = float(self.balance) + float(value)
        self.addTransaction(
            Transaction(
                        source=source,
                        receptor=self.name1,
                        value=value,
                        dateTransaction= datetime.now(),
                        concluded=True,
                        typeTransaction="receive pix",
                        idTransaction=self.idLastTransaction + 1,
                        bankReceptor=self.bank,
                        bankSource=bankSourceName
                    )
        )
        self.operationLock.release()
        return 1


    def sendPix(self, value, url, keyPixReceptor, receptorName):
        self.operationLock.acquire()
        if(float(self.balance) < float(value)):
            return "Not money availible for this transaction", 0
        elif(keyPixReceptor == self.keyPix):
            return "error, key is same of client", 0
        else: #verificar se a chave nao é a do mesmo usuario
            #preparação para fazer o envio para o outro banco, ou para o outro usuario
            datasForSend = {}
            datasForSend["keyPix"] = keyPixReceptor
            datasForSend["value"] = value
            datasForSend["sender"] = self.cpfCNPJ1
            datasForSend["bankName"] = self.bank
            balanceBackup = self.balance
            try:
                infoReceivedByRequest = requests.patch(url, json = datasForSend)

                #atualizando as informações do sender
                self.balance = float(self.balance) - float(value)
                self.blockedBalance = float(self.blockedBalance) + float(value)
                self.addTransaction(
                    Transaction(
                            source=self.name1,
                            receptor=receptorName,
                            value=value,
                            dateTransaction= datetime.now(),
                            concluded=False,
                            typeTransaction="send pix",
                            idTransaction=self.idLastTransaction + 1,
                            bankReceptor= "None",
                            bankSource=self.bank
                        )
                )
                
                #verificando como foi a recepção desse dinheiro
                if(infoReceivedByRequest.status_code == 200): #deu certo receber o dinheiro
                    self.blockedBalance = float(self.blockedBalance) - float(value)
                    self.transactions[self.idLastTransaction].concluded = True
                    self.operationLock.release()
                    return "money send with sucess", 1
                else:
                    self.blockedBalance = float(self.blockedBalance) - float(value)
                    self.balance = float(self.balance) + float(value)
                    self.transactions[self.idLastTransaction].concluded = "error"
                    self.operationLock.release()
                    return "error in requisition", 0
            
            except:
                self.operationLock.release()
                self.balance = balanceBackup
                return "error in transaction", 406
            
