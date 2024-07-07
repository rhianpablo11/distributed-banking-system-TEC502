import threading
from transactionModel import Transaction
from datetime import *
import requests

class Account:
    def __init__(self, name1, name2, cpfCNPJ1, cpfCNPJ2, email, password, isFisicAccount, accountNumber, telephone, bank, isJoinetAccount, balance, blockedBalance, listBanks):
        self.email = email
        self.password = password
        self.isJoinetAccount = isJoinetAccount
        self.isFisicAccount = isFisicAccount
        self.id = hash(cpfCNPJ1)
        self.keyPix = cpfCNPJ1
        self.accountNumber = accountNumber
        self.telephone = telephone
        self.bank = bank
        self.balance = balance
        self.blockedBalance = blockedBalance
        self.transactions = {}
        self.idLastTransaction = 0
        self.operationLock = threading.Lock()
        self.listBanks = listBanks
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
            "blockedBalance": self.blockedBalance,
            "banksList": self.listBanks
        }
        listTransactions = []
        for transaction in self.transactions:
            listTransactions.append(self.transactions[transaction].getJsonTransaction())
        listTransactions.reverse()
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
        print(datetime.now())
        self.balance = float(self.balance) + float(value) 
        self.addTransaction(
            Transaction(
                        nameSource=self.name1,
                        cpfCPNJSource=self.cpfCNPJ1,
                        nameReceiver=self.name1,
                        cpfCPNJReceiver=self.cpfCNPJ1,
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
        return 1


    def receivePix(self, data):
        self.operationLock.acquire()
        self.blockedBalance = float(self.blockedBalance) + float(data['value'])
        self.addTransaction(
            Transaction(
                        nameSource=data['nameSender'],
                        cpfCPNJSource=data['cpfCNPJSender'],
                        nameReceiver=self.name1,
                        cpfCPNJReceiver=self.cpfCNPJ1,
                        value=data['value'],
                        dateTransaction= datetime.now(),
                        concluded="pending",
                        typeTransaction="receive Pix",
                        idTransaction=self.idLastTransaction + 1,
                        bankReceptor=self.bank,
                        bankSource=data['bankSourceName']
                    )
        )
        self.operationLock.release()
        return (1, (self.idLastTransaction))


    def sendPix(self, url, data):
        self.operationLock.acquire()
        if(float(self.balance) < float(data["value"])): #verificar se tem saldo
            self.operationLock.release()
            return ("Not money availible for this transaction", 0)
        elif((data["keyPix"] == self.keyPix) and (data['bankNameReceiver'])==self.bank): #verificar se a chave nao é a do mesmo usuario
            self.operationLock.release()
            return ("error, key is same of client", 0)
        else: 
            balanceBackup = self.balance
            blockedBalanceBackup = self.blockedBalance
            try:
                print("AAAAAAA")
                infoReceivedByRequest = requests.patch(url, json = data)
                #atualizando as informações do sender
                print("BBBBBBBBBBBB")
                self.balance = float(self.balance) - float(data["value"])
                self.blockedBalance = float(self.blockedBalance) + float(data["value"])
                self.addTransaction(
                    Transaction(
                            nameSource=self.name1,
                            cpfCPNJSource=self.cpfCNPJ1,
                            nameReceiver= data["nameReceiver"],
                            cpfCPNJReceiver= data['keyPix'],
                            value=data['value'],
                            dateTransaction= datetime.now(),
                            concluded="pending",
                            typeTransaction="send Pix",
                            idTransaction=self.idLastTransaction + 1,
                            bankReceptor=data['bankNameReceiver'],
                            bankSource=data["bankSourceName"]
                        )
                )
                print("CCCCCCCC")
                print(infoReceivedByRequest)
                dataReceived = infoReceivedByRequest
                
                #verificando como foi a recepção desse dinheiro
                if(infoReceivedByRequest.status_code == 200): #deu certo receber o dinheiro
                    self.operationLock.release()
                    dataReceivedJson = dataReceived.json()
                    return ("money send with sucess", 200, (self.idLastTransaction),dataReceivedJson['idTransaction'])
                else:
                    self.blockedBalance = float(self.blockedBalance) - float(data['value'])
                    self.balance = float(self.balance) + float(data['value'])
                    self.transactions[self.idLastTransaction].concluded = "error"
                    self.operationLock.release()
                    return ("error in requisition", 400)
            
            except:
                self.operationLock.release()
                self.balance = balanceBackup
                self.blockedBalance = blockedBalanceBackup
                self.addTransaction(
                    Transaction(
                            nameSource=self.name1,
                            cpfCPNJSource=self.cpfCNPJ1,
                            nameReceiver= data["nameReceiver"],
                            cpfCPNJReceiver= data['keyPix'],
                            value=data['value'],
                            dateTransaction= datetime.now(),
                            concluded="error",
                            typeTransaction="send Pix",
                            idTransaction=self.idLastTransaction + 1,
                            bankReceptor=data['bankNameReceiver'],
                            bankSource=data["bankSourceName"]
                        )
                )
                return ("error in transaction", 406)
            

    def addBankToList(self, bankName):
        self.operationLock.acquire()
        if(bankName not in self.listBanks):
            self.listBanks.append(bankName)
        self.operationLock.release()


    def concludedTransaction(self, idTransaction):
        self.operationLock.acquire()
        self.transactions[idTransaction].concluded = True
        if(self.transactions[idTransaction].typeTransaction == 'receive Pix'):
            self.blockedBalance = float(self.blockedBalance) - float(self.transactions[idTransaction].value)
            self.balance = float(self.transactions[idTransaction].value) + float(self.balance)
            self.transactions[idTransaction].concluded= True

        else:
            self.blockedBalance = float(self.blockedBalance) - float(self.transactions[idTransaction].value)
        self.transactions[idTransaction].concluded= True
        self.operationLock.release()


    def errorTransaction(self, idTransaction):

        self.operationLock.acquire()
        if(self.transactions[idTransaction].typeTransaction == 'receive Pix'):
            print('RETIRANDO')
            print('antes: ', self.blockedBalance)
            self.blockedBalance = float(self.blockedBalance) - float(self.transactions[idTransaction].value)
            print('depois: ', self.blockedBalance)
        else:
            self.balance = float(self.transactions[idTransaction].value) + float(self.balance)
            self.blockedBalance = float(self.blockedBalance) - float(self.transactions[idTransaction].value)
        self.transactions[idTransaction].concluded = "error"
        self.operationLock.release()