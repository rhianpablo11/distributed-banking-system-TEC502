import threading
from token_control import token
from storage import network_storage

def make_operation_after_receiver_token():
    while True:
        if(token.get_if_has_token()):
            key_to_operate = network_storage.get_operation_to_make()
            if(key_to_operate != None):
                operate_operation_received(key_to_operate)
                token.pass_token_to_other_host()
                

def operate_operation_received(operation_key):
    pass