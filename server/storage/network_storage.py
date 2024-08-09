import threading

global address_banks
global self_id
global operations_to_make
operations_lock = threading.Lock()

address_banks = {
    '0': [-1, 'eleven'],
    '1': [-1, 'automobili'],
    '2': [-1, 'formula'],
    '3': [-1, 'secret'],
    '4': [-1, 'titanium']
}
self_id = -1
operations_to_make = []


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


def get_operation_to_make():
    operations_lock.acquire()
    if(len(operations_to_make)>0):
        operations_lock.release()
        return(operations_to_make[0])
    operations_lock.release()
    return None


def add_operation(operation_to_add):
    global operations_to_make
    operations_lock.acquire()
    operations_to_make.append(operation_to_add)
    operations_to_make[len(operations_to_make)-1]['index_operation'] = len(operations_to_make) - 1
    operations_lock.release()


def remove_operation(operation_to_delete):
    global operations_to_make
    operations_lock.acquire()
    if(len(operations_to_make)>=operation_to_delete['index_operation']):
        del operations_to_make[operation_to_delete['index_operation']]
    operations_lock.release()