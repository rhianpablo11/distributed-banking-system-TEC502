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

