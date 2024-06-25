class Transaction:
    def __init__(self, source, receptor, value, dateTransaction, concluded, typeTransaction, idTransaction, bankReceptor, bankSource, idTransactionExternal):
        self.source = source
        self.receptor = receptor
        self.value = value
        self.dateTransaction = dateTransaction
        self.concluded = concluded
        self.typeTransaction = typeTransaction
        self.idTransaction = idTransaction
        self.bankReceptor = bankReceptor
        self.bankSource = bankSource
        self.idTransactionExternal = idTransactionExternal

    def getJsonTransaction(self):
        
        auxJson = {
            "source": self.source,
            "receptor":self.receptor,
            "value": self.value,
            "dateTransaction": self.dateTransaction,
            "concluded": self.concluded,
            "typeTransaction": self.typeTransaction,
            "bankSource": self.bankSource,
            "bankReceptor": self.bankReceptor
        }
        return auxJson
        