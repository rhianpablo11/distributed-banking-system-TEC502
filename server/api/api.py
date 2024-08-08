from flask_cors import CORS
from flask import *
from storage import accounts_storage, network_storage

app = Flask(__name__)
CORS(app)
app.run("0.0.0.0", 10000, debug=False, threaded=True)

@app.route("/account/search/<int:account_number>", methods=['POST'])
def search_account(account_number):
    account_found = accounts_storage.find_account_by_number_account(account_number)
    if (account_found == None):
        return 'account not found', 404
    return make_response(jsonify(accounts_storage.find_account_by_number_account(account_number).get_json_basic_data())), 200


@app.route('/bank', methods=['GET'])
def get_name_bank():
    name_bank = network_storage.get_name_bank()
    if(name_bank != None):
        return make_response(jsonify({'name_bank': name_bank})), 200
    return 'error internal', 500


@app.route('/account/transaction/info/<string:type_transfer>', methods=['POST'])
def get_basic_info_account(type_transfer):
    data_received_with_requisition = request.json
    data_to_send = None
    if(type_transfer != 'ted' or type_transfer != 'pix'):
        return 'type transfer not recognized', 406
    elif(type_transfer == 'ted'):
        data_to_send = accounts_storage.find_account_by_number_account(data_received_with_requisition['account_number']).get_json_basic_data()
    elif(type_transfer == 'pix'):
        data_to_send = accounts_storage.find_account_by_key_pix(data_received_with_requisition['key_pix']).get_json_basic_data()
    if(data_to_send != None):
        return make_response(jsonify(data_to_send)), 200
    else:
        return 'account not found', 404
    

@app.route('/account/user/<:document_user>/update-profile/change/telephone', methods=['PATCH'])
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
    

@app.route('/account/user/<:document_user>/update-profile/change/email', methods=['PATCH'])
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


@app.route('/account/user/<:document_user>/update-profile/change/password', methods=['PATCH'])
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
    return make_response(jsonify({'id_transaction': return_the_operation[1]}))


@app.route('/account/invest/<:type_investiment>/<float:value>', methods=['POST'])
def invest_money(type_investiment, value):
    pass


@app.route('/account/<:type_investiment>/<float:value>', methods=['POST'])
def withdraw_money(type_investiment, value):
    pass