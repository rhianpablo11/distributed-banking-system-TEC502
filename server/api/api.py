import requests
from flask_cors import CORS
from flask import *
from storage import accounts_storage, network_storage
from models import user
from token_control import token

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


@app.route('/account/login', methods=['POST'])
def login_account():
    data_received_with_requisition = request.json
    account_found = accounts_storage.find_account_by_number_account(data_received_with_requisition['account_number'])
    if(account_found == None):
        return 'account not found', 404
    if(len(account_found.user_list)>1):
        if(account_found.user_list[0].password == user.cryptography_password(data_received_with_requisition['password'])):
            return make_response(jsonify(account_found.get_json_user_logged(0))), 200
        elif(account_found.user_list[1].password == user.cryptography_password(data_received_with_requisition['password'])):
            return make_response(jsonify(account_found.get_json_user_logged(1))), 200
        else:
            return 'password incorrect', 406
    if(account_found.user_list[0].password == user.cryptography_password(data_received_with_requisition['password'])):
        return make_response(jsonify(account_found.get_json_user_logged(0))), 200
    return 'password incorrect', 406
    

@app.route('/account/transaction/info/<string:type_transfer>', methods=['POST'])
def get_basic_info_account(type_transfer):
    data_received_with_requisition = request.json
    data_to_send = None
    if(type_transfer != 'ted' or type_transfer != 'pix'):
        return 'type transfer not recognized', 400
    elif(type_transfer == 'ted'):
        data_to_send = accounts_storage.find_account_by_number_account(data_received_with_requisition['account_number']).get_json_basic_data()
    elif(type_transfer == 'pix'):
        data_to_send = accounts_storage.find_account_by_key_pix(data_received_with_requisition['key_pix']).get_json_basic_data()
    if(data_to_send != None):
        return make_response(jsonify(data_to_send.get_json_basic_data())), 200
    else:
        return 'account not found', 404
    

@app.route('/account/request-info-account/<string:type_transfer>', methods=['POST'])
def request_basic_info_other_account(type_transfer):
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
        data_received_by_request = requests.post(url=url_to_communicated, json=data_to_send)
        if(data_received_by_request.status_code == 200):
            data_received_by_request_json = data_received_by_request.json
            return make_response(jsonify(data_received_by_request_json)), 200
        elif(data_received_by_request.status_code == 404):
            return 'account researched not found', 404
        else:
            return 'error in request', 400


@app.route('/user/infos', methods=['POST'])
def get_info_user():
    data_received_with_requisition = request.json
    data_of_search = accounts_storage.find_user_by_document(data_received_with_requisition['document'])
    if(data_of_search != None):
        return make_response(jsonify(data_of_search.get_json())), 200
    return 'user not found', 404


@app.route('/user/<:document_user>/update-profile/change/telephone', methods=['PATCH'])
def change_telephone_user(document_user):
    data_received_with_requisition = request.json
    user_to_update = accounts_storage.find_user_by_document(document_user)
    if(user_to_update == None):
        return 'user not found', 404
    else:
        if(user_to_update.change_telephone(data_received_with_requisition['new_telephone'])):
            if(accounts_storage.save_user_after_changes(user_to_update)):
                return 'update make with success', 200
            else:
                return 'user not found, or error internal', 400
        else:
            return 'telephone is same the registered', 409
    

@app.route('/user/<:document_user>/update-profile/change/email', methods=['PATCH'])
def change_email_user(document_user):
    data_received_with_requisition = request.json
    user_to_update = accounts_storage.find_user_by_document(document_user)
    if(user_to_update == None):
        return 'user not found', 404
    else:
        if(user_to_update.change_email(data_received_with_requisition['new_email'])):
            if(accounts_storage.save_user_after_changes(user_to_update)):
                return 'update make with success', 200
            else:
                return 'user not found, or error internal', 400
        else:
            return 'email is same the registered', 409


@app.route('/user/<:document_user>/update-profile/change/password', methods=['PATCH'])
def change_password_user(document_user):
    data_received_with_requisition = request.json
    user_to_update = accounts_storage.find_user_by_document(document_user)
    if(user_to_update == None):
        return 'user not found', 404
    else:
        return_the_operation = user_to_update.change_password(data_received_with_requisition['new_password'])
        if(return_the_operation[0]):
            if(accounts_storage.save_user_after_changes(user_to_update)):
                return 'update make with success', 200
            else:
                return 'user not found, or error internal', 400
        else:
            return return_the_operation[1], 409
        

@app.route('/account/receive-money/<:method_receive>', methods=['POST'])
def receive_money(method_receive):
    data_received_with_requisition = request.json
    return_the_operation = None
    if(method_receive == 'ted' or method_receive == 'pix'):
        return_the_operation = accounts_storage.find_account_by_number_account(data_received_with_requisition['account_number']).receive_transfer_money(
            data_received_with_requisition['value'],
            data_received_with_requisition['name_source'],
            data_received_with_requisition['document_source'],
            data_received_with_requisition['account_number_source'],
            data_received_with_requisition['bank_source'],
            method_receive
        )
    elif(method_receive == 'deposit'):
        return_the_operation = accounts_storage.find_account_by_number_account(data_received_with_requisition['account_number']).receive_deposit(
            data_received_with_requisition['value']
        )
    return make_response(jsonify({'id_transaction': return_the_operation[1]})), 200


@app.route('/account/trasfer/<:type_transfer>/<int:account_number>', methods=['POST'])
def transfer_money(type_transfer, account_number):
    data_received_with_requisition = request.json
    account_source_infos = accounts_storage.find_account_by_number_account(account_number)
    operation_to_put_in_dict = {
        'type_operation': 'transfer',
        'index_operation': -1,
        'executed': False,
        'response': -1,
        'code_response': -1,
        'data_to_operate': {
            'value': data_received_with_requisition['value'],
            'name_source': account_source_infos.user_list[0].name,
            'document_source': account_source_infos.user_list[0].document,
            'account_number_source': account_number,
            'bank_source': account_source_infos.name_bank,
            'type_transaction': type_transfer
        }
    }
    operation_key = network_storage.add_operation(operation_to_put_in_dict)
    if(network_storage.verify_operation_state(operation_key) == True):
        operation_conclusion = network_storage.find_operation_by_key(operation_key)
        if(operation_conclusion != None):
            return operation_conclusion['response'], operation_conclusion['code_response']
        else:
            return 'error in operation', 500
    else:
        return 'error in operation', 500


@app.route('/account/invest/<:type_investiment>/<float:value>/<int:account_number>', methods=['POST'])
def invest_money(type_investiment, value, account_number):
    operation_to_put_in_dict = {
            'type_operation': 'investiment',
            'index_operation': -1,
            'executed': False,
            'response': -1,
            'code_response': -1,
            'data_to_operate': {
                'value': value,
                'account_number': account_number,
                'type_investiment': type_investiment
            }
        }
    operation_key = network_storage.add_operation(operation_to_put_in_dict)
    if(network_storage.verify_operation_state(operation_key) == True):
        operation_conclusion = network_storage.find_operation_by_key(operation_key)
        if(operation_conclusion != None):
            return operation_conclusion['response'], operation_conclusion['code_response']
        else:
            return 'error in operation', 500
    else:
        return 'error in operation', 500


@app.route('/account/withdraw/<:type_investiment>/<float:value>/<int:account_number>', methods=['POST'])
def withdraw_money(type_investiment, value, account_number):
    operation_to_put_in_dict = {
            'type_operation': 'withdraw_investiment',
            'index_operation': -1,
            'executed': False,
            'response': -1,
            'code_response': -1,
            'data_to_operate': {
                'value': value,
                'account_number': account_number,
                'type_investiment': type_investiment
            }
        }
    operation_key = network_storage.add_operation(operation_to_put_in_dict)
    if(network_storage.verify_operation_state(operation_key) == True):
        operation_conclusion = network_storage.find_operation_by_key(operation_key)
        if(operation_conclusion != None):
            return operation_conclusion['response'], operation_conclusion['code_response']
        else:
            return 'error in operation', 500
    else:
        return 'error in operation', 500


