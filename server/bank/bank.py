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

    user_list_to_account = []
    account_number_genereted = accounts_storage.generate_new_account_number()

    user_0 = accounts_storage.find_user_by_document(operation_data['document_user_0'])

    #nao encontrou o usuario nesse banco e tem que criar um novo
    if(user_0 == None):
        new_user_0 = user.User(
                name= operation_data['name_user_0'],
                document= operation_data['document_user_0'],
                telephone= operation_data['telephone_user_0'],
                email= operation_data['email_user_0'],
                is_company=operation_data['is_company'],
                password= operation_data['password_user_0'],
                banks_with_account= search_user_in_other_banks(operation_data['document_user_0'], account_number_genereted)
            )
        accounts_storage.add_new_user(new_user_0)
        user_list_to_account.append(new_user_0.document)

    elif(user_0 != None): #achou o user
        #pegar a lista de numeros de conta que o usuario possui naquele banco
        accounts_number_found = user_0.banks_with_account[network_storage.get_name_bank()] 
        
        #realizar verificação
        for account_number in accounts_number_found:
            #achou uma conta conjunta
            if(len(accounts_storage.find_account_by_number_account(account_number).user_list) > 1):
                #verificar se essa conta conjunta é com os usuarios passados como parametro para esta função
                quantity_user_match = 0
                for document_user in accounts_storage.find_account_by_number_account(account_number).user_list:
                    if(document_user == user_0.document):
                        quantity_user_match += 1
                    if(operation_data['is_joint_account']):
                        if(document_user == operation_data['document_user_1']):
                            quantity_user_match += 1

                if(quantity_user_match >= 2):
                    return 'account with this two users already in system', 409
            
            # esse usuario ja possui uma conta sozinho, e esta tentando criar outra conta sozinho
            elif(not operation_data['is_joint_account']):
                return 'user already in bank', 409
        user_list_to_account.append(user_0.document)
        user_0.add_new_bank_to_list(name_bank=network_storage.get_name_bank(), account_number_in_the_bank=account_number_genereted)
        accounts_storage.update_user_after_changes(user_0)

    if(operation_data['is_joint_account']):
        user_1 = accounts_storage.find_user_by_document(operation_data['document_user_1'])
        if(user_1 == None):
            new_user_1 = user.User(
                name= operation_data['name_user_1'],
                document= operation_data['document_user_1'],
                telephone= operation_data['telephone_user_1'],
                email= operation_data['email_user_1'],
                is_company= False,
                password= operation_data['password_user_1'],
                banks_with_account= search_user_in_other_banks(operation_data['document_user_1'], account_number_genereted)
            )
            user_list_to_account.append(new_user_1.document)
            accounts_storage.add_new_user(new_user_1)
        else:
            user_list_to_account.append(user_1)
            user_1.add_new_bank_to_list(name_bank=network_storage.get_name_bank(), account_number_in_the_bank=account_number_genereted)
            accounts_storage.update_user_after_changes(user_1)

    new_account = account.Account(
        user_list= user_list_to_account,
        account_number= accounts_storage.generate_new_account_number(),
        bank_name= network_storage.get_name_bank(),
    )


    accounts_storage.add_new_account(new_account)

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


def search_user_in_other_banks(document_user, new_account_number):
    banks_not_replied = []
    banks_with_account = {}
    self_id = network_storage.get_id()
    next_bank_to_communicate = str(int(self_id) + 1)
    while next_bank_to_communicate != self_id:
        try:
            if(int(next_bank_to_communicate) > 5):
                next_bank_to_communicate = '0'
            if(next_bank_to_communicate == self_id):
                break
            address_bank_to_communicate = network_storage.find_address_bank_by_id(next_bank_to_communicate)
            url_base = f'{address_bank_to_communicate}/user/search/{document_user}/{new_account_number}/{network_storage.get_name_bank()}'
            data_received_by_request = requests.post(url=url_base)
            data_received_by_request_json = data_received_by_request.json()
            if(data_received_by_request.status_code == 200):
                banks_with_account[data_received_by_request_json['bank_name']] = data_received_by_request_json['accounts_number_of_this_user']
            
            next_bank_to_communicate = str(int(next_bank_to_communicate) + 1)
        except:
            banks_not_replied.append(network_storage.find_name_bank_by_id(next_bank_to_communicate))
            next_bank_to_communicate = str(int(next_bank_to_communicate) + 1)
            
    return banks_with_account