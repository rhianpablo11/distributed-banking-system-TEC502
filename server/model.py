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
        if(isJoinetAccount):
            self.name1 = name1
            self.cpfCNPJ1 = cpfCNPJ1
            self.name2 = name2
            self.cpfCNPJ2 = cpfCNPJ2
        else:
            self.name1 = name1
            self.cpfCNPJ1 = cpfCNPJ1
    

    def jsonComplet(self):
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
        return auxJson
    

    def infoBasic(self):
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
        return auxJson
        

    def setKeyPix(self, active):
        if(active == "True"):
            self.keyPix = self.cpfCNPJ1
        else:
            self.keyPix = None

    def setBalance(self, newBalance):
        self.balance = newBalance
    
    def setBlockedBalance(self, blockedValue):
        oldBlocked = float(self.blockedBalance)
        oldBlocked += blockedValue
        self.blockedBalance = oldBlocked