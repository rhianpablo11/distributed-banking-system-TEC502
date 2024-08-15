from models import account, user

accounts = {}
accounts_number = account.GenerateNumberAccountBank()
users = {}


def get_accounts():
    return accounts


def get_users():
    return users


def add_new_user(new_user):
    users[new_user.document] = new_user
    return users[new_user.document].get_json()


def add_new_account(new_account):
    accounts[new_account.account_number] = new_account
    return new_account.get_json()


def generate_new_account_number():
    account_number = accounts_number.createAccountNumber()


def find_user_by_document(document_search) -> user.User:
    if(document_search in users):
        return users[document_search]
    else:
        return None
    

def find_account_by_number_account(account_number) -> account.Account:
    if(account_number in accounts):
        return accounts[account_number]
    else:
        return None
    

def find_account_by_document_user(document_search) -> list:
    accounts_found = []
    for account in accounts:
        for user in accounts[account].user_list:
            if(user.document == document_search):
                accounts_found.append(accounts[account])
    return accounts_found


def get_accounts_number_of_this_user(document_search) -> list:
    accounts_number_found = []
    for account in accounts:
        for user in account.user_list:
            if(user == document_search):
                accounts_number_found.append(account.account_number)
    return accounts_number_found
            


def find_account_by_key_pix(key_pix_search) -> account.Account:
    for account in accounts:
        if(accounts[account].key_pix == key_pix_search):
            return accounts[account]
    return None


def update_account_after_changes(account_to_save):
    if (account_to_save.account_number in accounts):
        accounts[account_to_save.account_number] = account_to_save
        return 1
    return None


def update_user_after_changes(user_to_save):
    if(user_to_save.document in users):
        users[user_to_save.document] = user_to_save
        return 1
    return None


def add_account_number_to_user(document_user, account_number_to_add, name_bank):
    if(document_user in users):
        users[document_user].add_new_bank_to_list(name_bank, account_number_to_add)
        return 1
    return None