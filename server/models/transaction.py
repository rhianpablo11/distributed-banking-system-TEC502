class Transaction:
    def __init__(self, nameSource,cpfCPNJSource, nameReceiver, cpfCPNJReceiver, value, dateTransaction, concluded, typeTransaction, idTransaction, bankReceptor, bankSource):
        self.nameSource = nameSource
        self.cpfCPNJSource = cpfCPNJSource
        self.nameReceiver = nameReceiver
        self.cpfCPNJReceiver = cpfCPNJReceiver
        self.value = value
        self.dateTransaction = dateTransaction
        self.concluded = concluded
        self.typeTransaction = typeTransaction
        self.idTransaction = idTransaction
        self.bankReceptor = bankReceptor
        self.bankSource = bankSource

    def getJsonTransaction(self):
        
        auxJson = {
            "source": self.nameSource,
            "receptor":self.nameReceiver,
            "value": self.value,
            "dateTransaction": self.dateTransaction,
            "concluded": self.concluded,
            "typeTransaction": self.typeTransaction,
            "bankSource": self.bankSource,
            "bankReceptor": self.bankReceptor,
            "idTransaction": self.idTransaction
        }
        return auxJson
        