import random
import threading
import requests
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
        json_user = []
        for user in self.user_list:
            json_user.append(user.get_json())
        return  {
            'balance': self.balance,
            'account_number': self.account_number,
            'blocked_balance': self.blocked_balance,
            'transactions': list_json_transactions,
            'users': json_user
        }
        
    
    def get_json_transactions(self):
        list_json_transactions = []
        if(len(self.transactions) >0):
             for transaction in self.transactions:
                   list_json_transactions.append(self.transactions[transaction].get_json())
        list_json_transactions.reverse()
        return {'transactions': list_json_transactions}
    

    def get_json_basic_data(self):
        document_masked = self.user_list[0].document
        if len(document_masked) == 14 and document_masked[3] == '.' and document_masked[7] == '.' and document_masked[11] == '-':
            document_masked = '***.' + document_masked[4:7] + '.' + document_masked[8:11] + '-**'
        return  {
            'name': self.user_list[0].name,
            'document': document_masked,
            'name_bank': self.name_bank,
            'account_number': self.account_number
        }


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
        return 1, new_transaction['id_transaction']
        

    def receive_transfer_money(self, value, name_source, document_source, account_number_source, bank_source, type_transaction):
        self.operation_lock.acquire()
        self.blocked_balance += value
        new_transaction = transaction.Transaction(
                name_source= name_source,
                document_source= document_source,
                account_number_source= account_number_source,
                name_receiver= self.user_list[0].name,
                document_receiver= self.user_list[0].document,
                account_number_receiver= self.account_number,
                value= value,
                concluded= 'peding',
                type_transaction= type_transaction,
                id_transaction= self.id_last_transaction,
                bank_receptor= self.name_bank,
                bank_source= bank_source
            )
        self.transactions[self.id_last_transaction] = new_transaction
        self.id_last_transaction += 1
        self.operation_lock.release()
        return 1, new_transaction['id_transaction']
    

    def transfer_money_ted(self, url, value, name_receiver, document_receiver, account_number_receiver, bank_receiver):
        self.operation_lock.acquire()
        if(value > self.balance):
            self.operation_lock.release()
            return 0, 'not money available to this transaction'
        elif(account_number_receiver == self.account_number and bank_receiver == self.name_bank):
            self.operation_lock.release()
            return 0, 'not possible transfer money to your account in this bank'
        else:
            try:
                data_to_send = {
                    'value': value,
                    'name_source': self.user_list[0].name,
                    'document_source': self.user_list[0].document,
                    'account_number_source': self.account_number,
                    'bank_source': self.name_bank
                }

                self.balance -= value
                self.blocked_balance += value

                new_transaction = transaction.Transaction(
                        name_source= self,
                        document_source= self.user_list[0].document,
                        account_number_source= self.account_number,
                        name_receiver= name_receiver,
                        document_receiver= document_receiver,
                        account_number_receiver= account_number_receiver,
                        value= value,
                        concluded= 'peding',
                        type_transaction= 'send_ted',
                        id_transaction= self.id_last_transaction,
                        bank_receptor= bank_receiver,
                        bank_source= self.name_bank
                    )
                self.transactions[self.id_last_transaction] = new_transaction
                self.id_last_transaction += 1

                data_received_by_request = requests.post(url = url, json = data_to_send)
                if(data_received_by_request.status_code == 200):
                    data_received_json = data_received_by_request.json()
                    self.operation_lock.release()
                    return 1, 'money transfer with success', {
                        'id_transaction_sender': new_transaction.id_transaction,
                        'id_transaction_receiver': data_received_json['id_transaction']}
                else:
                    self.blocked_balance -= value
                    self.balance += value
                    self.transactions[self.id_last_transaction].concluded = 'error'
                    self.operation_lock.release()
                    return 0, 'error in transfer money'
            except:
                self.blocked_balance -= value
                self.balance += value
                self.transactions[self.id_last_transaction].concluded = 'error'
                self.operation_lock.release()
                return 0, 'error in transfer money'
            
    
    def confirmate_transaction(self, id_transaction):
        self.operation_lock.acquire()
        try:
            self.transactions[id_transaction].concluded = True
            if(self.transactions[id_transaction].type_transaction == 'send_ted' or self.transactions[id_transaction].type_transaction == "send_pix"):
                self.blocked_balance -= self.transactions[id_transaction].value
                self.operation_lock.release()
            else:
                self.balance += self.transactions[id_transaction].value
                self.blocked_balance -= self.transactions[id_transaction].value
                self.operation_lock.release()
            return 1
        except:
            self.operation_lock.release()
            return 0


    def cancel_transaction(self, id_transaction):
        self.operation_lock.acquire()
        try:
            self.transactions[id_transaction].concluded = True
            if(self.transactions[id_transaction].type_transaction == 'send_ted' or self.transactions[id_transaction].type_transaction == "send_pix"):
                self.balance += self.transactions[id_transaction].value
                self.blocked_balance -= self.transactions[id_transaction].value
                self.operation_lock.release()
            else:
                self.blocked_balance -= self.transactions[id_transaction].value
                self.operation_lock.release()
            return 1
        except:
            self.operation_lock.release()
            return 0
        



class GenerateNumberAccountBank:
    def __init__(self):
        self.accountNumbersInSystem = set()


    def createAccountNumber(self):
            while True:
                accountNumber = random.randint(0000, 99999)
                if accountNumber not in self.accountNumbersInSystem:
                    self.accountNumbersInSystem.add(accountNumber)
                    return accountNumber