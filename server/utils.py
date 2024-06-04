from hashlib import sha512


def cryptographyPassword(password):
    encryptedPassword = sha512(password.encode()).digest()
    return encryptedPassword


