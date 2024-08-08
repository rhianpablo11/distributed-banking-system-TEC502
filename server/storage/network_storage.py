global address_banks
global self_id
address_banks = {
    '0': [-1, 'eleven'],
    '1': [-1, 'automobili'],
    '2': [-1, 'formula'],
    '3': [-1, 'secret'],
    '4': [-1, 'titanium']
}

self_id = -1

def get_id():
    return self_id


def get_name_bank():
    if(self_id != -1):
        return address_banks[self_id][1]
    return None


def set_address_bank(id_bank, address):
    global address_banks
    address_banks[id_bank][0] = address


def set_self_id(id_to_set):
    global self_id
    self_id = id_to_set