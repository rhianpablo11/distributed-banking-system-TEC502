import random
import threading
from models import transaction


class Account:
    def __init__(self, user_list, account_number, bank_name):
        self.user_list = user_list
        self.balance = 0
        self.blocked_balance = 0
        self.cdi_balance = 0 #investimento com maior rendimento
        self.saving_balance = 0 #investimento seguro e com menor rendimento
        self.key_pix = ''
        self.account_number = account_number
        self.name_bank = bank_name
        self.transactions = {}
        self.id_last_transaction = 0
        self.operation_lock = threading.Lock()


    def get_json(self):
        list_json_transactions = []
        if(len(self.transactions) >0):
             for transaction in self.transactions:
                   list_json_transactions.append(self.transactions[transaction].get_json())
        list_json_transactions.reverse()

        aux_json = {
            'balance': self.balance,
            'account_number': self.account_number,
            'blocked_balance': self.blocked_balance,
            'transactions': list_json_transactions,
            'users': self.user_list
        }
        return aux_json
    

    def get_json_transactions(self):
        list_json_transactions = []
        if(len(self.transactions) >0):
             for transaction in self.transactions:
                   list_json_transactions.append(self.transactions[transaction].get_json())
        list_json_transactions.reverse()
        return {'transactions': list_json_transactions}
    

    def invest_money_cdi(self, value):
        self.operation_lock.acquire()
        if(self.balance < value):
            self.operation_lock.release()
            return 0, 'not money available'
        else:
            self.balance -= value
            self.cdi_balance += value
            new_transaction = transaction.Transaction(
                name_source= self.user_list[0].name,
                document_source= self.user_list[0].document,
                account_number_source= self.account_number,
                name_receiver= self.user_list[0].name,
                document_receiver= self.user_list[0].document,
                account_number_receiver= self.account_number,
                value= value,
                concluded= True,
                type_transaction= 'investiment_cdi',
                id_transaction= self.id_last_transaction,
                bank_receptor= self.name_bank,
                bank_source= self.name_bank
            )
            self.transactions[self.id_last_transaction] = new_transaction
            self.id_last_transaction += 1
            self.operation_lock.release()
            return 1, 'money invested with success'


    def withdraw_money_cdi(self, value):
        self.operation_lock.acquire()
        if(self.cdi_balance < value):
            self.operation_lock.release()
            return 0, 'not money invested available'
        else:
            self.cdi_balance -= value
            self.balance += value
            new_transaction = transaction.Transaction(
                name_source= self.user_list[0].name,
                document_source= self.user_list[0].document,
                account_number_source= self.account_number,
                name_receiver= self.user_list[0].name,
                document_receiver= self.user_list[0].document,
                account_number_receiver= self.account_number,
                value= value,
                concluded= True,
                type_transaction= 'withdraw_cdi',
                id_transaction= self.id_last_transaction,
                bank_receptor= self.name_bank,
                bank_source= self.name_bank
            )
            self.transactions[self.id_last_transaction] = new_transaction
            self.id_last_transaction += 1
            self.operation_lock.release()
            return 1, 'money returned to your wallet'


    #para gerar rendimentos via CDI - investimento em tesouro - possui 1% de rendimento
    def income_cdi(self):
        self.operation_lock.acquire()
        if(self.cdi_balance > 0 ):
            money_earned_with_investiment = self.cdi_balance * 0.01
            new_transaction = transaction.Transaction(
                name_source= self.user_list[0].name,
                document_source= self.user_list[0].document,
                account_number_source= self.account_number,
                name_receiver= self.user_list[0].name,
                document_receiver= self.user_list[0].document,
                account_number_receiver= self.account_number,
                value= money_earned_with_investiment,
                concluded= True,
                type_transaction= 'earned_investiment_cdi',
                id_transaction= self.id_last_transaction,
                bank_receptor= self.name_bank,
                bank_source= self.name_bank
            )
            self.cdi_balance += money_earned_with_investiment
            self.transactions[self.id_last_transaction] = new_transaction
            self.id_last_transaction += 1
        self.operation_lock.release()


    def invest_money_saving(self, value):
        self.operation_lock.acquire()
        if(self.balance < value):
            self.operation_lock.release()
            return 0, 'not money available'
        else:
            self.balance -= value
            self.saving_balance += value
            new_transaction = transaction.Transaction(
                name_source= self.user_list[0].name,
                document_source= self.user_list[0].document,
                account_number_source= self.account_number,
                name_receiver= self.user_list[0].name,
                document_receiver= self.user_list[0].document,
                account_number_receiver= self.account_number,
                value= value,
                concluded= True,
                type_transaction= 'investiment_saving',
                id_transaction= self.id_last_transaction,
                bank_receptor= self.name_bank,
                bank_source= self.name_bank
            )
            self.transactions[self.id_last_transaction] = new_transaction
            self.id_last_transaction += 1
            self.operation_lock.release()
            return 1, 'money invested with success'


    def withdraw_money_saving(self, value):
        self.operation_lock.acquire()
        if(self.saving_balance < value):
            self.operation_lock.release()
            return 0, 'not money invested available'
        else:
            self.saving_balance -= value
            self.balance += value
            new_transaction = transaction.Transaction(
                name_source= self.user_list[0].name,
                document_source= self.user_list[0].document,
                account_number_source= self.account_number,
                name_receiver= self.user_list[0].name,
                document_receiver= self.user_list[0].document,
                account_number_receiver= self.account_number,
                value= value,
                concluded= True,
                type_transaction= 'withdraw_saving',
                id_transaction= self.id_last_transaction,
                bank_receptor= self.name_bank,
                bank_source= self.name_bank
            )
            self.transactions[self.id_last_transaction] = new_transaction
            self.id_last_transaction += 1
            self.operation_lock.release()
            return 1, 'money returned to your wallet'
    
    
    #para gerar rendimentos na poupança possui 0.5% de rendimento
    def income_saving(self):
        self.operation_lock.acquire()
        if(self.saving_balance > 0 ):
            money_earned_with_investiment = self.saving_balance * 0.005
            new_transaction = transaction.Transaction(
                name_source= self.user_list[0].name,
                document_source= self.user_list[0].document,
                account_number_source= self.account_number,
                name_receiver= self.user_list[0].name,
                document_receiver= self.user_list[0].document,
                account_number_receiver= self.account_number,
                value= money_earned_with_investiment,
                concluded= True,
                type_transaction= 'earned_investiment_saving',
                id_transaction= self.id_last_transaction,
                bank_receptor= self.name_bank,
                bank_source= self.name_bank
            )
            self.saving_balance += money_earned_with_investiment
            self.transactions[self.id_last_transaction] = new_transaction
            self.id_last_transaction += 1
        self.operation_lock.release()
    

    def receive_deposit(self, value):
        self.operation_lock.acquire()
        self.balance = float(self.balance) + value
        new_transaction = transaction.Transaction(
                name_source= self.user_list[0].name,
                document_source= self.user_list[0].document,
                account_number_source= self.account_number,
                name_receiver= self.user_list[0].name,
                document_receiver= self.user_list[0].document,
                account_number_receiver= self.account_number,
                value= value,
                concluded= True,
                type_transaction= 'deposit',
                id_transaction= self.id_last_transaction,
                bank_receptor= self.name_bank,
                bank_source= self.name_bank
            )
        self.transactions[self.id_last_transaction] = new_transaction
        self.id_last_transaction += 1
        self.operation_lock.release()
        



class GenerateNumberAccountBank:
    def __init__(self):
        self.accountNumbersInSystem = set()


    def createAccountNumber(self):
            while True:
                accountNumber = random.randint(0000, 99999)
                if accountNumber not in self.accountNumbersInSystem:
                    self.accountNumbersInSystem.add(accountNumber)
                    return accountNumber