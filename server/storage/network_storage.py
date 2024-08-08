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
