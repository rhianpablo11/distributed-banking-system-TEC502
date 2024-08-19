import requests
import datetime
import jwt
from flask_cors import CORS
from flask import *
from storage import accounts_storage, network_storage, keys_storage
from models import user
from token_control import token
from functools import wraps
from api import authenticate

app = Flask(__name__)
CORS(app)


@app.route('/bank', methods=['GET'])
def get_name_bank():
    name_bank = network_storage.get_name_bank()
    if(name_bank != None):
        return make_response(jsonify({'name_bank': name_bank})), 200
    return 'error internal', 500


@app.route('/token', methods=['POST'])
def receive_token():
    data_received_with_requisition = request.json
    self_couter = token.get_my_value_of_counter()
    self_id_int = int(network_storage.get_id())
    if(data_received_with_requisition['counter_all_banks'][self_id_int] >= self_couter):
        token.set_new_counter_token_all_banks(data_received_with_requisition['counter_all_banks'])
        token.set_has_token(True)
        token.add_self_counter()
        return 'token recepted, and everything ok', 200
    else:
        return 'were you disconnected', 409
    

@app.route("/account/search/<int:account_number>", methods=['POST'])
def search_account(account_number):
    account_found = accounts_storage.find_account_by_number_account(account_number)
    if (account_found == None):
        return 'account not found', 404
    return make_response(jsonify(accounts_storage.find_account_by_number_account(account_number).get_json_basic_data())), 200


@app.route('/user/search/<string:document_user_to_search>/<int:account_number_to_add>/<string:name_bank>', methods=['POST'])
def search_user(document_user_to_search, account_number_to_add, name_bank):
    user_found = accounts_storage.find_user_by_document(document_user_to_search)
    if(user_found == None):
        return 'user not found', 404
    else:
        accounts_storage.add_account_number_to_user(document_user_to_search, name_bank, account_number_to_add)
        return make_dict_to_json_response({
            'bank_name': network_storage.get_name_bank(),
            'accounts_number_of_this_user': accounts_storage.get_accounts_number_of_this_user(document_user_to_search)
        }), 200


@app.route('/account/login', methods=['POST'])
def login_account():
    data_received_with_requisition = request.json
    account_found = accounts_storage.find_account_by_number_account(data_received_with_requisition['account_number'])
    if(account_found == None):
        return 'account not found', 404
    if(len(account_found.user_list)>1):
        for document_user_in_account in account_found.user_list:
            user_of_interation = accounts_storage.find_user_by_document(document_user_in_account)
            if(user_of_interation != None and user_of_interation.password == user.cryptography_password(data_received_with_requisition['password'])):
                account_found.set_logged_into_account(True)
                accounts_storage.update_account_after_changes(account_found)
                payload = {
                        'account_number': account_found.account_number,
                        'document_user_logged': document_user_in_account,
                        'expiration': str(datetime.datetime.utcnow() + datetime.timedelta(minutes=1))
                }

                token_jwt = jwt.encode(payload, keys_storage.get_jwt_secret_key())

                data_to_return = {
                    'account_info':account_found.get_json_user_logged(account_found.user_list.index(document_user_in_account)),
                    'token_jwt': token_jwt
                }
                return make_response(jsonify(data_to_return)), 200
        else:
            return 'password incorrect', 406
    if(accounts_storage.find_user_by_document(account_found.user_list[0]).password == user.cryptography_password(data_received_with_requisition['password'])):
        account_found.set_logged_into_account(True)
        accounts_storage.update_account_after_changes(account_found)
        payload = {
            'account_number': account_found.account_number,
            'document_user_logged': account_found.user_list[0],
            'expiration': str(datetime.datetime.utcnow() + datetime.timedelta(minutes=1))
        }

        token_jwt = jwt.encode(payload, keys_storage.get_jwt_secret_key())

        return make_response(jsonify({'account_info': account_found.get_json_user_logged(0), 'token': token_jwt})), 200
    return 'password incorrect', 406
    

@app.route('/account/logged')
@authenticate.jwt_token_required
def get_account_full_info_for_user_logged(account_number_logged, document_user_logged):
    account_found = accounts_storage.find_account_by_number_account(account_number_logged)
    if(account_found == None):
        return 'account not found', 404
    
    return make_response(jsonify(account_found.get_json_user_logged(account_found.user_list.index(document_user_logged))))



@app.route('/account/logout', methods=['POST'])
@authenticate.jwt_token_required
def logout_account(account_number_logged, document_user_logged):
    account_found = accounts_storage.find_account_by_number_account(account_number_logged)
    if(account_found == None):
        return 'account not found', 404
    else:
        account_found.set_logged_into_account(False)
        accounts_storage.update_account_after_changes(account_found)
        return 'logout with success', 200


@app.route('/account/transaction/info/<string:type_transfer>', methods=['POST'])
def get_basic_info_account(type_transfer):
    data_received_with_requisition = request.json
    data_to_send = None
    if(type_transfer != 'ted' and type_transfer != 'pix'):
        return 'type transfer not recognized', 400
    elif(type_transfer == 'ted'):
        data_to_send = accounts_storage.find_account_by_number_account(data_received_with_requisition['account_number'])
    elif(type_transfer == 'pix'):
        data_to_send = accounts_storage.find_account_by_key_pix(data_received_with_requisition['key_pix'])
    if(data_to_send != None):
        return make_response(jsonify(data_to_send.get_json_basic_data())), 200
    else:
        return 'account not found', 404
    

@app.route('/account/request-info-account/<string:type_transfer>', methods=['POST'])
@authenticate.jwt_token_required
def request_basic_info_other_account(account_number_logged, document_user_logged, type_transfer ):
    data_received_with_requisition = request.json
    address_bank_found = network_storage.find_address_bank_by_id(data_received_with_requisition['id_bank'])
    if(address_bank_found == None):
        return 'id bank not recognized', 400
    elif(type_transfer == 'ted' or type_transfer == 'pix'):
        return 'type transaction not reconized', 400
    else:
        url_to_communicated = f'{address_bank_found}/account/transaction/info/{data_received_with_requisition['type_transfer']}'
        if(type_transfer == 'ted'):
            data_to_send = {
                'account_number': data_received_with_requisition['account_number']
            }
        elif(type_transfer == 'pix'):
            data_to_send = {
                'key_pix': data_received_with_requisition['key_pix']
            }
        try:
            data_received_by_request = requests.post(url=url_to_communicated, json=data_to_send)
            if(data_received_by_request.status_code == 200):
                data_received_by_request_json = data_received_by_request.json
                return make_response(jsonify(data_received_by_request_json)), 200
            elif(data_received_by_request.status_code == 404):
                return 'account researched not found', 404
        except:
            return 'error in request', 400


@app.route('/user/infos', methods=['POST'])
@authenticate.jwt_token_required
def get_info_user(account_number_logged, document_user_logged):
    data_of_search = accounts_storage.find_user_by_document(document_user_logged)
    if(data_of_search != None):
        return make_response(jsonify(data_of_search.get_json())), 200
    return 'user not found', 404


@app.route('/user/update-profile/change/telephone', methods=['PATCH'])
@authenticate.jwt_token_required
def change_telephone_user(account_number_logged, document_user_logged):
    data_received_with_requisition = request.json
    user_to_update = accounts_storage.find_user_by_document(document_user_logged)
    if(user_to_update == None):
        return 'user not found', 404
    else:
        if(user_to_update.change_telephone(data_received_with_requisition['new_telephone'])):
            if(accounts_storage.update_user_after_changes(user_to_update)):
                return 'update make with success', 200
            else:
                return 'user not found, or error internal', 400
        else:
            return 'telephone is same the registered', 409
    

@app.route('/user/<string:document_user>/update-profile/change/email', methods=['PATCH'])
@authenticate.jwt_token_required
def change_email_user(account_number_logged, document_user_logged):
    data_received_with_requisition = request.json
    user_to_update = accounts_storage.find_user_by_document(document_user_logged)
    if(user_to_update == None):
        return 'user not found', 404
    else:
        if(user_to_update.change_email(data_received_with_requisition['new_email'])):
            if(accounts_storage.update_user_after_changes(user_to_update)):
                return 'update make with success', 200
            else:
                return 'user not found, or error internal', 400
        else:
            return 'email is same the registered', 409


@app.route('/user/<string:document_user>/update-profile/change/password', methods=['PATCH'])
@authenticate.jwt_token_required
def change_password_user(account_number_logged, document_user_logged):
    data_received_with_requisition = request.json
    user_to_update = accounts_storage.find_user_by_document(document_user_logged)
    if(user_to_update == None):
        return 'user not found', 404
    else:
        return_the_operation = user_to_update.change_password(data_received_with_requisition['new_password'])
        if(return_the_operation[0]):
            if(accounts_storage.update_user_after_changes(user_to_update)):
                return 'update make with success', 200
            else:
                return 'user not found, or error internal', 400
        else:
            return return_the_operation[1], 409
        
#verificar isso, pq o receber deposito ta aq dentro
@app.route('/account/receive-money/<string:method_receive>', methods=['POST'])
def receive_money(method_receive):
    data_received_with_requisition = request.json
    return_the_operation = None
    if(method_receive == 'ted' or method_receive == 'pix'):
        account_found = accounts_storage.find_account_by_number_account(data_received_with_requisition['account_number'])
        return_the_operation = account_found.receive_transfer_money(
            data_received_with_requisition['value'],
            data_received_with_requisition['name_source'],
            data_received_with_requisition['document_source'],
            data_received_with_requisition['account_number_source'],
            data_received_with_requisition['bank_source'],
            method_receive
        )
        return make_response(jsonify({'id_transaction': return_the_operation[1]})), 200  
    else:
        return 'operation not recognized', 400


@app.route('/account/deposit/<float:value>', methods=['POST'])
@authenticate.jwt_token_required
def receive_deposit(account_number_logged, document_user_logged, value):
    account_found = accounts_storage.find_account_by_number_account(account_number_logged)
    if(account_found == None):
        return 'account not found', 404

    if(not accounts_storage.verify_user_in_account(document_user_to_search=document_user_logged,
                                               account_to_verify=account_number_logged)):
        return 'user not match in account', 404

    operation_to_put_in_dict = {
            'type_operation': 'deposit',
            'index_operation': -1,
            'executed': False,
            'code_response': -1,
            'response': -1,
            'data_to_operate': {
                'value': value,
                'account_number': account_number_logged,
                'document_user_logged': document_user_logged
            }
        }
    
    operation_key = network_storage.add_operation(operation_to_put_in_dict)
    if(network_storage.verify_operation_state(operation_key) == True):
        return_the_operation = network_storage.find_operation_by_key(operation_key)
        network_storage.remove_operation(operation_key)
        if(return_the_operation != None):
            return return_the_operation['response'], return_the_operation['code_response']
        else:
            return 'error in operation', 500
    else:
        return 'error in operation', 500


#melhorar isso dentro do modelo da conta
@app.route('/account/transfer/<string:type_transfer>/', methods=['POST'])
@authenticate.jwt_token_required
def transfer_money(account_number_logged, document_user_logged, type_transfer):
    data_received_with_requisition = request.json
    account_source_infos = accounts_storage.find_account_by_number_account(account_number_logged)
    if(account_source_infos == None):
        return 'account not found', 404
    
    if(not accounts_storage.verify_user_in_account(document_user_to_search=document_user_logged,
                                               account_to_verify=account_number_logged)):
        return 'user not match in account', 404
    

    operation_to_put_in_dict = {
        'type_operation': 'transfer',
        'index_operation': -1,
        'executed': False,
        'response': -1,
        'code_response': -1,
        'data_to_operate': {
            'value': data_received_with_requisition['value'],
            'bank_receiver': data_received_with_requisition['name_bank'],
            'name_receiver': data_received_with_requisition['name'],
            'account_number_receiver': data_received_with_requisition['account_number'],
            'document_receiver':  data_received_with_requisition['document_receiver'],
            'type_transaction': type_transfer,
            'key_pix':  data_received_with_requisition['key_pix'],
            'account_number_source': account_number_logged,
            'document_user_logged': document_user_logged
        }
    }
    operation_key = network_storage.add_operation(operation_to_put_in_dict)
    if(network_storage.verify_operation_state(operation_key) == True):
        operation_conclusion = network_storage.find_operation_by_key(operation_key)
        network_storage.remove_operation(operation_key)
        if(operation_conclusion != None):
            return operation_conclusion['response'], operation_conclusion['code_response']
        else:
            return 'error in operation', 500
    else:
        return 'error in operation', 500


@app.route('/account/confirmation-operation/<int:id_transaction_to_confirm>/<int:account_number>', methods=['POST'])
def confirmate_transaction_of_account_client(id_transaction_to_confirm, account_number):
    account_to_operate = accounts_storage.find_account_by_number_account(account_number)
    if(account_to_operate == None):
        return 'account not found', 404
    
    if(account_to_operate.confirmate_transaction(id_transaction_to_confirm)):
        accounts_storage.update_account_after_changes(account_to_operate)
        return 'operation confirmated with success', 200
    else:
        return 'error in confirmate operation', 400


@app.route('/account/cancel-operation/<int:id_transaction_to_cancel>/<int:account_number>', methods=['POST'])
def cancel_transaction_of_account_client(id_transaction_to_cancel, account_number):
    account_to_operate = accounts_storage.find_account_by_number_account(account_number)
    if(account_to_operate == None):
        return 'account not found', 404
    
    if(account_to_operate.cancel_transaction(id_transaction_to_cancel)):
        accounts_storage.update_account_after_changes(account_to_operate)
        return 'operation canceled with success', 200
    else:
        return 'error in confirmate operation', 400


@app.route('/account/invest/<string:type_investiment>/<float:value>', methods=['POST'])
@authenticate.jwt_token_required
def invest_money(account_number_logged, document_user_logged, type_investiment, value):
    account_source_infos = accounts_storage.find_account_by_number_account(account_number_logged)
    if(account_source_infos == None):
        return 'account not found', 404
    
    if(not accounts_storage.verify_user_in_account(document_user_to_search=document_user_logged,
                                               account_to_verify=account_number_logged)):
        return 'user not match in account', 404

    operation_to_put_in_dict = {
            'type_operation': 'investiment',
            'index_operation': -1,
            'executed': False,
            'response': -1,
            'code_response': -1,
            'data_to_operate': {
                'value': value,
                'account_number': account_number_logged,
                'type_investiment': type_investiment,
                'document_user_logged': document_user_logged
            }
        }
    operation_key = network_storage.add_operation(operation_to_put_in_dict)
    if(network_storage.verify_operation_state(operation_key) == True):
        operation_conclusion = network_storage.find_operation_by_key(operation_key)
        network_storage.remove_operation(operation_key)
        if(operation_conclusion != None):
            return operation_conclusion['response'], operation_conclusion['code_response']
        else:
            return 'error in operation', 500
    else:
        return 'error in operation', 500


@app.route('/account/withdraw/<string:type_investiment>/<float:value>/<int:account_number>', methods=['POST'])
@authenticate.jwt_token_required
def withdraw_money(account_number_logged, document_user_logged, type_investiment, value ):
    account_source_infos = accounts_storage.find_account_by_number_account(account_number_logged)
    if(account_source_infos == None):
        return 'account not found', 404
    
    if(not accounts_storage.verify_user_in_account(document_user_to_search=document_user_logged,
                                               account_to_verify=account_number_logged)):
        return 'user not match in account', 404

    operation_to_put_in_dict = {
            'type_operation': 'withdraw_investiment',
            'index_operation': -1,
            'executed': False,
            'response': -1,
            'code_response': -1,
            'data_to_operate': {
                'value': value,
                'account_number': account_number_logged,
                'type_investiment': type_investiment,
                'document_user_logged': document_user_logged
            }
        }
    operation_key = network_storage.add_operation(operation_to_put_in_dict)
    if(network_storage.verify_operation_state(operation_key) == True):
        operation_conclusion = network_storage.find_operation_by_key(operation_key)
        network_storage.remove_operation(operation_key)
        if(operation_conclusion != None):
            return operation_conclusion['response'], operation_conclusion['code_response']
        else:
            return 'error in operation', 500
    else:
        return 'error in operation', 500


@app.route('/account/create', methods=['POST'])
def create_new_account():
    data_received_with_requisition = request.json
    operation_to_put_in_dict = {
        'type_operation': 'create',
        'index_operation': -1,
        'executed': False,
        'response': -1,
        'code_response': -1,
        'data_to_operate': {
            'name_user_0': data_received_with_requisition['name_user_0'],
            'document_user_0': data_received_with_requisition['document_user_0'],
            'telephone_user_0': data_received_with_requisition['telephone_user_0'],
            'email_user_0': data_received_with_requisition['email_user_0'],
            'password_user_0': data_received_with_requisition['password_user_0'],
            'is_company': data_received_with_requisition['is_company'],
            'is_joint_account': data_received_with_requisition['is_joint_account'],
            'name_user_1': data_received_with_requisition['name_user_1'],
            'document_user_1': data_received_with_requisition['document_user_1'],
            'telephone_user_1': data_received_with_requisition['telephone_user_1'],
            'email_user_1': data_received_with_requisition['email_user_1'],
            'password_user_1': data_received_with_requisition['password_user_1'],
        }
    }

    operation_key = network_storage.add_operation(operation_to_put_in_dict)
    if(network_storage.verify_operation_state(operation_key) == True):
        return_the_operation = network_storage.find_operation_by_key(operation_key)
        network_storage.remove_operation(operation_key)
        if(return_the_operation != None):
            return return_the_operation['response'], return_the_operation['code_response']
        else:
            return 'error in operation', 500
    else:
        return 'error in operation', 500


def make_dict_to_json_response(dict_to_convert):
    print(dict_to_convert)
    if(type(dict_to_convert) == dict):
        return make_response(jsonify(dict_to_convert))
    return None