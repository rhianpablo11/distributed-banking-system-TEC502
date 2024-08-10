import threading

global address_banks
global self_id
global operations_to_make
global last_id_operation
operations_lock = threading.Lock()

address_banks = {
    '0': [-1, 'eleven'],
    '1': [-1, 'automobili'],
    '2': [-1, 'formula'],
    '3': [-1, 'secret'],
    '4': [-1, 'titanium']
}
self_id = -1
last_id_operation = 0
operations_to_make = {}


def get_id():
    return self_id


def get_name_bank():
    if(self_id != -1):
        return address_banks[self_id][1]
    return None


def find_address_bank_by_id(id_bank):
    if(int(id_bank) > 4 or int(id_bank) < 0):
        return address_banks[id_bank][0]
    else:
        return None

def find_name_bank_by_id(id_bank):
    if(int(id_bank) > 4 or int(id_bank) < 0):
        return address_banks[id_bank][1]
    else:
        return None


def set_address_bank(id_bank, address):
    global address_banks
    address_banks[id_bank][0] = address


def set_self_id(id_to_set):
    global self_id
    self_id = id_to_set


def get_operation_to_make():
    operations_lock.acquire()
    if(len(operations_to_make)>0):
        operations_lock.release()
        return(next(iter(operations_to_make)))
    operations_lock.release()
    return None


def get_last_id_operation():
    return last_id_operation


def add_operation(operation_to_add):
    global operations_to_make
    global last_id_operation
    operations_lock.acquire()
    operation_to_add['index_operation'] = get_last_id_operation() + 1
    operations_to_make[operation_to_add['index_operation']] = operation_to_add
    last_id_operation += 1
    operations_lock.release()
    return operation_to_add['index_operation'] #retorno da chave em que esta a operação


def remove_operation(operation_to_delete):
    global operations_to_make
    operations_lock.acquire()
    if(operation_to_delete in operations_to_make):
        del operations_to_make[operation_to_delete['index_operation']]
    operations_lock.release()


def verify_operation_state(index_operation_to_verify):
    if(index_operation_to_verify in operations_to_make):
        while(operations_to_make[index_operation_to_verify]['executed'] == False):
            pass
        return True
    return None


def find_operation_by_key(key_operation_to_search):
    if(key_operation_to_search in operations_to_make):
        return {
            'response': operations_to_make[key_operation_to_search]['response'],
            'code_response': operations_to_make[key_operation_to_search]['code_response']
        }
    return None