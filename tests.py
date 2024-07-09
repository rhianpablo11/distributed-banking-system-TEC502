import requests
import json
import threading
import random
import string
import json

accountsToCreate = [
    {
        "operation": "create",
        "clientCpfCNPJ": "190.038.470-10",
        "dataOperation":{
            "name1": "Rhian Pablo",
            "cpfCNPJ1": "190.038.470-10",
            "name2": "",
            "cpfCNPJ2": "",
            "email": "rhian@gmail.com",
            "password":"12345678",
            "telephone": "75999999",
            "isFisicAccount": "True",
            "isJoinetAccount": "False"
        }
    },
    {
        "operation": "create",
        "clientCpfCNPJ": "651.551.749-10",
        "dataOperation":{
            "name1": "Sebastião Igor Iago Lopes",
            "cpfCNPJ1": "651.551.749-10",
            "name2": "",
            "cpfCNPJ2": "",
            "email": "sebastiao_lopes@capgemini.com",
            "password":"12345678",
            "telephone": "75999999",
            "isFisicAccount": "True",
            "isJoinetAccount": "False"
        }
    },
    {
        "operation": "create",
        "clientCpfCNPJ": "966.545.144-83",
        "dataOperation":{
            "name1": "Daiane Eloá Kamilly Moraes",
            "cpfCNPJ1": "966.545.144-83",
            "name2": "",
            "cpfCNPJ2": "",
            "email": "daiane_eloa_moraes@agnet.com.br",
            "password":"12345678",
            "telephone": "75999999",
            "isFisicAccount": "True",
            "isJoinetAccount": "False"
        }
    },
    {
        "operation": "create",
        "clientCpfCNPJ": "368.862.614-10",
        "dataOperation":{
            "name1": "Giovana Clarice Sarah Cardoso",
            "cpfCNPJ1": "368.862.614-10",
            "name2": "",
            "cpfCNPJ2": "",
            "email": "giovanaclaricecardoso@libbero.com.br",
            "password":"12345678",
            "telephone": "75999999",
            "isFisicAccount": "True",
            "isJoinetAccount": "False"
        }
    },
    {
        "operation": "create",
        "clientCpfCNPJ": "985.110.925-87",
        "dataOperation":{
            "name1": "Renato Renan Moura",
            "cpfCNPJ1": "985.110.925-87",
            "name2": "",
            "cpfCNPJ2": "",
            "email": "renato_moura@grupomozue.com.br",
            "password":"12345678",
            "telephone": "75999999",
            "isFisicAccount": "True",
            "isJoinetAccount": "False"
        }
    },
    {
        "operation": "create",
        "clientCpfCNPJ": "552.237.366-05",
        "dataOperation":{
            "name1": "Pietra Tânia Nair Baptista",
            "cpfCNPJ1": "552.237.366-05",
            "name2": "",
            "cpfCNPJ2": "",
            "email": "pietrataniabaptista@damataemporionatural.com.br",
            "password":"12345678",
            "telephone": "75999999",
            "isFisicAccount": "True",
            "isJoinetAccount": "False"
        }
    }
]


depositAccounts = [
    {
        "operation": "deposit",
        "clientCpfCNPJ": "190.038.470-10",
        "dataOperation":{
            "value": 20000,
            "method": "money"
        }
    },
    {
        "operation": "deposit",
        "clientCpfCNPJ": "651.551.749-10",
        "dataOperation":{
            "value": 20000,
            "method": "money"
        }
    },
    {
        "operation": "deposit",
        "clientCpfCNPJ": "966.545.144-83",
        "dataOperation":{
            "value": 20000,
            "method": "money"
        }
    },
    {
        "operation": "deposit",
        "clientCpfCNPJ":"368.862.614-10",
        "dataOperation":{
            "value": 20000,
            "method": "money"
        }
    },
    {
        "operation": "deposit",
        "clientCpfCNPJ": "552.237.366-05",
        "dataOperation":{
            "value": 20000,
            "method": "money"
        }
    }
]



# Função para gerar um nome aleatório
def generate_random_name():
    first_names = ['João', 'Maria', 'José', 'Ana', 'Pedro', 'Paula', 'Lucas', 'Mariana', 'Rafael', 'Bianca']
    last_names = ['Silva', 'Santos', 'Oliveira', 'Pereira', 'Souza', 'Lima', 'Almeida', 'Ferreira', 'Costa', 'Rodrigues']
    return f"{random.choice(first_names)} {random.choice(first_names)} {random.choice(last_names)}"

# Função para gerar um CPF/CNPJ aleatório (formato simples)
def generate_random_cpf():
    return '{}.{}.{}-{}'.format(
        ''.join(random.choices(string.digits, k=3)),
        ''.join(random.choices(string.digits, k=3)),
        ''.join(random.choices(string.digits, k=3)),
        ''.join(random.choices(string.digits, k=2))
    )

# Função para gerar um email aleatório baseado no nome
def generate_random_email(name):
    domain = random.choice(['gmail.com', 'hotmail.com', 'yahoo.com', 'example.com', 'test.com'])
    email = f"{name.replace(' ', '.').lower()}@{domain}"
    return email

# Função para gerar dados de teste
def generate_test_data(num_tests):
    accounts_to_create = []
    deposit_accounts = []
    pix_operations = []
    
    banks = ["Automobili", "Eleven", "Formula", "Secret", "Titanium"]
    
    for _ in range(num_tests):
        name = generate_random_name()
        cpf_cnpj = generate_random_cpf()
        email = generate_random_email(name)
        
        create_operation = {
            "operation": "create",
            "clientCpfCNPJ": cpf_cnpj,
            "dataOperation": {
                "name1": name,
                "cpfCNPJ1": cpf_cnpj,
                "name2": "",
                "cpfCNPJ2": "",
                "email": email,
                "password": "12345678",
                "telephone": "75999999",
                "isFisicAccount": "True",
                "isJoinetAccount": "False"
            }
        }
        
        deposit_operation = {
            "operation": "deposit",
            "clientCpfCNPJ": cpf_cnpj,
            "dataOperation": {
                "value": random.randint(1000, 50000),  # Valor de depósito entre 1000 e 50000
                "method": "money"
            }
        }
        
        accounts_to_create.append(create_operation)
        deposit_accounts.append(deposit_operation)
    
    # Gerar operações de PIX
    for i in range(num_tests // 2):
        sender_index = random.randint(0, num_tests - 1)
        receiver_index = (sender_index + random.randint(1, num_tests - 1)) % num_tests
        
        sender_cpf_cnpj = accounts_to_create[sender_index]["clientCpfCNPJ"]
        receiver_cpf_cnpj = accounts_to_create[receiver_index]["clientCpfCNPJ"]
        receiver_name = accounts_to_create[receiver_index]["dataOperation"]["name1"]
        
        pix_operation = {
            "operation": "sendPix",
            "clientCpfCNPJ": sender_cpf_cnpj,
            "dataOperation": {
                "value": random.randint(100, 10000),  # Valor de PIX entre 100 e 10000
                "keyPix": receiver_cpf_cnpj,
                "idBank": str(random.randint(1, 5)),  # idBank de 1 a 5
                "nameReceiver": receiver_name,
                "bankNameReceiver": random.choice(banks)
            }
        }
        
        pix_operations.append(pix_operation)
    
    return accounts_to_create, deposit_accounts, pix_operations

# Gerar 10 dados de teste
num_tests = 10
accounts_to_create, deposit_accounts, pix_operations = generate_test_data(num_tests)

# Exibir os dados de teste
print("Accounts to Create:")
print(json.dumps(accounts_to_create, indent=2))

print("\nDeposit Accounts:")
print(json.dumps(deposit_accounts, indent=2))

print("\nPIX Operations:")
print(json.dumps(pix_operations, indent=2))


addressToSend = [0,0,0,0,0]

addressToSend[0] = input('DIGITE O 1º ENDEREÇO: ')
addressToSend[1] = input('DIGITE O 2º ENDEREÇO: ')
addressToSend[2] = input('DIGITE O 3º ENDEREÇO: ')
addressToSend[3] = input('DIGITE O 4º ENDEREÇO: ')
addressToSend[4] = input('DIGITE O 5º ENDEREÇO: ')

# addressToSend[0] = 'localhost:8081'
# addressToSend[1] = 'localhost:8082'
# addressToSend[2] = 'localhost:8083'
# addressToSend[3] = 'localhost:8084'
# addressToSend[4] = 'localhost:8085'




threads = []

def sendOperation(dataAccount, address):
    try:
        url = f"http://{address}/operations"
        print(f"CNPJ DA VEZ: {dataAccount['clientCpfCNPJ']}\n")
        print(f"URL: {url}")
        print(f"Data: {dataAccount}")

        response = requests.post(url, json=dataAccount)

        # Checa se a resposta foi bem sucedida
        if response.status_code == 200:
            print(f"Request bem sucedida.\nOperação: {dataAccount['operation']}\nHOST: {address}")
        else:
            print(f"Falha na request. Status Code: {response.status_code}\nOperação: {dataAccount['operation']}\nHOST: {address}")
            print(f"Resposta: {response.text}\nOperação: {dataAccount['operation']}\nHOST: {address}")
            
        return response

    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro na requisição: {e}")


'''
    CRIANDO CONTAS
'''

for account in accounts_to_create:
    for address in addressToSend:
        thread = threading.Thread(target=sendOperation, args=(account, address))
        threads.append(thread)

print(f'FORAM ADICIONADAS {len(threads)} THREADS PARA ENVIAR')

for t in threads:
    t.start()

for thread in threads:
    thread.join()


print('FINALIZADO AS CRIAÇÕES')
'''
    DEPOSITANDO DINHEIRO
'''
threads = []

for deposit in deposit_accounts:
    for address in addressToSend:
        thread = threading.Thread(target=sendOperation, args=(deposit, address))
        threads.append(thread)

for t in threads:
    t.start()

for thread in threads:
    thread.join()

print('FINALIZADO OS DEPOSITOS')
threads = []

for pix in pix_operations:
    for address in addressToSend:
        thread = threading.Thread(target=sendOperation, args=(pix, address))
        threads.append(thread)

for t in threads:
    t.start()

for thread in threads:
    thread.join()

print('FINALIZADO OS PIX')