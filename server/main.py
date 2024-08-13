from api import api_bank
from storage import network_storage
from bank import bank
from token_control import token
import threading
import os


if(os.getenv('id_bank') != None and os.getenv('bank_0') != None and os.getenv('bank_1') != None and os.getenv('bank_2') != None and os.getenv('bank_3') != None and os.getenv('bank_4') != None):
    network_storage.set_self_id(os.getenv('id_bank'))
    network_storage.set_address_bank('0', os.getenv('bank_0'))
    network_storage.set_address_bank('1', os.getenv('bank_1'))
    network_storage.set_address_bank('2', os.getenv('bank_2'))
    network_storage.set_address_bank('3', os.getenv('bank_3'))
    network_storage.set_address_bank('4', os.getenv('bank_4'))


api_bank.app.run("0.0.0.0", 10000, debug=False, threaded=True)
threading.Thread(target=bank.make_operation_after_receiver_token, daemon=True).start()
if(network_storage.get_id() == '0'):
    token.set_has_token(True)
