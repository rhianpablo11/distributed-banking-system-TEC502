from hashlib import sha512
global jwt_secret_key
jwt_secret_key = ''

def set_jwt_secret_key(secret_key):
    global jwt_secret_key
    jwt_secret_key =  sha512(secret_key.encode()).hexdigest()


def get_jwt_secret_key():
    return jwt_secret_key