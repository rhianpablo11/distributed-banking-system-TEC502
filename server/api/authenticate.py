import jwt
from flask import request, current_app
from functools import wraps
from storage import keys_storage


def jwt_token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token_jwt = None
        if 'Authorization' in request.headers:
            token_jwt = request.headers['Authorization']

        if not token_jwt:
            return 'not permission to access this route', 403
        
        if not 'Bearer' in token_jwt:
            return 'token invalid', 401

        try:
            pure_token_jwt = token_jwt.replace('Bearer ', '')
            decoded_token_jwt = jwt.decode(jwt = pure_token_jwt,
                                           key = keys_storage.get_jwt_secret_key(),
                                           algorithms=['HS256'])
            account_number_logged = decoded_token_jwt['account_number']
            document_user_logged = decoded_token_jwt['document_user_logged']
            return func(account_number_logged, document_user_logged, *args, **kwargs)
        except Exception as e:
            return 'token invalid', 403
    return wrapper