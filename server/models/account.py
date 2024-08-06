import random


class Account:
    def __init__(self):
        self.name = 1


class GenerateNumberAccountBank:
    def __init__(self):
        self.accountNumbersInSystem = set()


    def createAccountNumber(self):
            while True:
                accountNumber = random.randint(0000, 99999)
                if accountNumber not in self.accountNumbersInSystem:
                    self.accountNumbersInSystem.add(accountNumber)
                    return accountNumber