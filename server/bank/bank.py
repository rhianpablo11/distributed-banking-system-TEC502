import threading
import requests
from token_control import token
from storage import network_storage, accounts_storage
from models import account, user
from api import api_bank

def make_operation_after_receiver_token():
    while True:
        if(token.get_if_has_token()):
            operation = network_storage.get_operation_to_make()
            if(operation != None):
                operate_operation_received(operation)
                token.pass_token_to_other_host()
            else:
                token.pass_token_to_other_host()


def operate_operation_received(operation_to_make):
    if(operation_to_make['type_operation'] == 'create'):
        operation_return = operation_create_account(operation_to_make['data_to_operate'])
        
    elif(operation_to_make['type_operation'] == 'invest'):
        operation_return = operation_invest_money(operation_to_make['data_to_operate'])
    
    elif(operation_to_make['type_operation'] == 'withdraw'):
        operation_return = operation_withdraw_investiment(operation_to_make['data_to_operate'])
    
    elif(operation_to_make['type_operation'] == 'deposit'):
        operation_return = operation_deposit_money(operation_to_make['data_to_operate'])
    
    elif(operation_to_make['type_operation'] == 'transfer'):
        operation_return = operation_transfer_money(operation_to_make['data_to_operate'])
    
    elif(operation_to_make['type_operation'] == 'packet_transfer'):
        operation_return = operation_packet_transfer(operation_to_make['data_to_operate'])

    else:
        operation_return = ['operation type not recognized', 406]

    operation_to_make['response'] = operation_return[0]
    operation_to_make['code_response'] = operation_return[1]
    operation_to_make['executed'] = True
    if(network_storage.update_operation(operation_to_make) != None):
        return 1
    else:
        return 0


def operation_create_account(operation_data):
    #retorno vai ter:
    # 1.Conseguiu criar:
    #    o json completo da conta e o codigo 200
    # 2. Nao conseguiu criar: 
    #    texto informando sobre e codigo 400
    if(accounts_storage.find_user_by_document(operation_data['document_user_0']) != None): #achou o user
        #verificar quantas contas esse user tem
        #verificar se ele ja tem uma conta so com ele sozinho
        #verificar se as outras contas conjuntas é com o outro possivel user da requisição
        pass
    else:
        user.User(
            name = operation_data['name_user_0'],
            document = operation_data['document_user_0'],
            telephone = operation_data['telephone_user_0'],
            email = operation_data['email_user_0'],
            password = operation_data['password_user_0'],
            is_company = operation_data['is_company'],
            banks_with_account = ,
        )



    new_account = account.Account(
        user_list= ,
        account_number= accounts_storage.generate_new_account_number(),
        bank_name= network_storage.get_name_bank(),
    )


    return_of_operation = accounts_storage.add_new_account(new_account)

    #caso em que conseguiu criar a conta
    response_to_return = api_bank.make_dict_to_json_response(new_account.get_json())
    if(response_to_return != None):
        return response_to_return, 200


def operation_invest_money(operation_data):
    account_to_operate = accounts_storage.find_account_by_number_account['account_number']
    if(account_to_operate == None):
        return 'account not found', 404
    else:
        if(operation_data['type_investiment'] == 'cdi'):
            if(account_to_operate.invest_money_cdi(operation_data['value'])):
                accounts_storage.update_account_after_changes(account_to_operate)
                return 'money invested with sucess', 200
            else:
                return 'not money available for investiment', 400
        elif(operation_data['type_investiment'] == 'saving'):
            if(account_to_operate.invest_money_saving(operation_data['value'])):
                accounts_storage.update_account_after_changes(account_to_operate)
                return 'money invested with sucess', 200
            else:
                return 'not money available for investiment', 400
        else:
            return 'type of investiment not recognized', 400
        
            
def operation_withdraw_investiment(operation_data):
    account_to_operate = accounts_storage.find_account_by_number_account['account_number']
    if(account_to_operate == None):
        return 'account not found', 404
    else:
        if(operation_data['type_investiment'] == 'cdi'):
            if(account_to_operate.withdraw_money_cdi(operation_data['value'])):
                accounts_storage.update_account_after_changes(account_to_operate)
                return 'withdraw money with sucess', 200
            else:
                return 'this value is more than available in investiment selected', 400
        elif(operation_data['type_investiment'] == 'saving'):
            if(account_to_operate.withdraw_money_saving(operation_data['value'])):
                accounts_storage.update_account_after_changes(account_to_operate)
                return 'withdraw money with sucess', 200
            else:
                return 'this value is more than available in investiment selected', 400
        else:
            return 'type of investiment not recognized', 400


def operation_deposit_money(operation_data):
    account_to_operate = accounts_storage.find_account_by_number_account(operation_data['account_number'])
    if(account_to_operate == None):
        return 'account not found', 404
    else:
        account_to_operate.receive_deposit(operation_data['value'])
        accounts_storage.update_account_after_changes(account_to_operate)
        return 'money add with success', 200
    

def operation_transfer_money(operation_data):
    pass


def operation_packet_transfer(operation_data):
    pass


def search_user_in_other_banks(document_user):
    pass