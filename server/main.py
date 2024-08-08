from api import api
from storage import network_storage
import os

network_storage.set_self_id(os.getenv('id_bank'))
network_storage.set_address_bank('0', os.getenv('bank_0'))
network_storage.set_address_bank('1', os.getenv('bank_1'))
network_storage.set_address_bank('2', os.getenv('bank_2'))
network_storage.set_address_bank('3', os.getenv('bank_3'))
network_storage.set_address_bank('4', os.getenv('bank_4'))


api.app.run("0.0.0.0", 10000, debug=False, threaded=True)