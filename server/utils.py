from hashlib import sha512
import random
import uuid


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

        
        