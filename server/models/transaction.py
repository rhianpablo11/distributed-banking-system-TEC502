import datetime

class Transaction:
    def __init__(self, name_source, document_source, account_number_source, name_receiver, document_receiver, account_number_receiver, value,  concluded, type_transaction, id_transaction, bank_receptor, bank_source):
        self.name_source = name_source
        self.document_source = document_source
        self.account_number_source = account_number_source
        self.name_receiver = name_receiver
        self.document_receiver = document_receiver
        self.account_number_receiver = account_number_receiver
        self.value = value
        self.date_transaction = datetime.datetime.now()
        self.concluded = concluded
        self.type_transaction = type_transaction
        self.id_transaction = id_transaction
        self.bank_receptor = bank_receptor
        self.bank_source = bank_source

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
        