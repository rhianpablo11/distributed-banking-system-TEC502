from api import api_bank
from storage import network_storage, accounts_storage
from bank import bank
from token_control import token
import threading
import os
import time


if(os.getenv('id_bank') != None and os.getenv('bank_0') != None and os.getenv('bank_1') != None and os.getenv('bank_2') != None and os.getenv('bank_3') != None and os.getenv('bank_4') != None):
    network_storage.set_self_id(os.getenv('id_bank'))
    network_storage.set_address_bank('0', os.getenv('bank_0'))
    network_storage.set_address_bank('1', os.getenv('bank_1'))
    network_storage.set_address_bank('2', os.getenv('bank_2'))
    network_storage.set_address_bank('3', os.getenv('bank_3'))
    network_storage.set_address_bank('4', os.getenv('bank_4'))

else:
    network_storage.set_self_id('0')
    network_storage.set_address_bank('0', 'http://localhost:10000')

def clear_terminal():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        print("Limpeza de terminal não suportada neste sistema.")



threading.Thread(target=api_bank.app.run, args=('0.0.0.0', 10000, False), daemon=True).start()
threading.Thread(target=bank.make_operation_after_receiver_token, daemon=True).start()
if(network_storage.get_id() == '0'):
    token.set_has_token(True)

while 1:
    print('==LIST USERS==')
    for account in accounts_storage.get_accounts():
        print(accounts_storage.find_account_by_number_account(account).get_json())
    print('==LIST OPERATIONS==')
    for operation in network_storage.get_operations():
        print(network_storage.find_operation_full_by_key(operation))
    time.sleep(3)




