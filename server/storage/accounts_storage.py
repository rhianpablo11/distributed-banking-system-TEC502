from models import account

accounts = {}
accounts_number = account.GenerateNumberAccountBank
users = {}


def get_accounts():
    return accounts

def get_users():
    return users

def add_new_account():
    account_number = accounts_number.createAccountNumber()
    new_account = account.Account()
    accounts[account_number] = new_account
    return new_account.get_json()

