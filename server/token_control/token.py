import requests
from storage import network_storage

global has_token
global counter_token_all_banks
counter_token_all_banks = []
has_token = False

def get_if_has_token():
    return has_token


def set_has_token(token: bool):
    global has_token
    has_token = token


def get_counter_token_all_banks() -> list:
    return counter_token_all_banks


def add_self_counter():
    global counter_token_all_banks
    counter_token_all_banks[int(network_storage.get_id())] += 1


def get_my_value_of_counter() -> int:
    return counter_token_all_banks[int(network_storage.get_id())]


def set_new_counter_token_all_banks(new_counter_to_save):
    global counter_token_all_banks
    counter_token_all_banks = new_counter_to_save


def set_my_value_in_counter(value):
    global counter_token_all_banks
    counter_token_all_banks[int(network_storage.get_id())] = value


def pass_token_to_other_host():
    bank_replied = False
    next_bank = int(network_storage.get_id()) + 1
    while not bank_replied:
        if(next_bank == int(network_storage.get_id())):
            next_bank = int(network_storage.get_id()) + 1
        if(next_bank > 4):
            next_bank = 0
        if(next_bank == int(network_storage.get_id())):
            next_bank = int(network_storage.get_id()) + 1
        
        data_to_send = {
            'bank_sender': network_storage.get_id(),
            'counter_all_banks': get_counter_token_all_banks()
        }

        url_to_communicated = f"{network_storage.find_address_bank_by_id(str(next_bank))}/token"

        try:
            set_has_token(False)
            data_received_by_requistion = requests.post(url=url_to_communicated, json=data_to_send, timeout=2)
            if(data_received_by_requistion.status_code == 200):
                bank_replied = True
            else:
                bank_replied = True
                set_my_value_in_counter(0)
        except:
            next_bank = int(network_storage.get_id()) + 1

