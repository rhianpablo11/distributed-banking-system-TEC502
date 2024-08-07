from models import account, user

accounts = {}
accounts_number = account.GenerateNumberAccountBank
users = {}


def get_accounts():
    return accounts


def get_users():
    return users


def add_new_user(name, document, telephone, email, password, is_company):
    users[document] = user.User(name, document, telephone, email, password, is_company)
    return users[document].get_json()


def add_new_account():
    account_number = accounts_number.createAccountNumber()
    new_account = account.Account()
    accounts[account_number] = new_account
    return new_account.get_json()


def find_user_by_document(document_search):
    if(document_search in users):
        return users[document_search]
    else:
        return 'user not found'
    

def find_account_by_number_account(account_number):
    if(account_number in accounts):
        return accounts[account_number]
    else:
        return 'account not found'
    

def find_account_by_document_user(document_search) -> list:
    accounts_found = []
    for account in accounts:
        for user in accounts[account].user_list:
            if(user.document == document_search):
                accounts_found.append(accounts[account])
    return accounts_found

