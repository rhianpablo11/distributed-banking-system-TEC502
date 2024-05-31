class Transaction:
    def __init__(self, source, receptor, value, dateTransaction, concluded, typeTransaction, idTransaction, bankReceptor, bankSource):
        self.source = source
        self.receptor = receptor
        self.value = value
        self.dateTransaction = dateTransaction
        self.concluded = concluded
        self.typeTransaction = typeTransaction
        self.idTransaction = idTransaction
        self.bankReceptor = bankReceptor
        self.bankSorce = bankSource

    def getJsonTransaction(self):
        auxJson = {
            "source": self.source,
            "value": self.value,
            "dateTransaction": self.dateTransaction,
            "concluded": self.concluded,
            "typeTransaction": self.typeTransaction,
            "bankSource": self.bankSource,
            "bankReceptor": self.bankReceptor
        }
        return auxJson
        