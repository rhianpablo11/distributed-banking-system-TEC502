from hashlib import sha512


global accountNumbers
accountNumbers = 2;

#função geradora de numero de conta conta
def createAccountNumber():
    global accountNumbers
    accountNumber = (accountNumbers**10+12*accountNumbers+(6*(accountNumbers**3)))/2
    accountNumbers +=2
    return accountNumber


def cryptographyPassword(password):
    encryptedPassword = sha512(password.encode()).digest()
    return encryptedPassword