import threading
import datetime
from hashlib import sha512

class User:
    def __init__(self, name, document, telephone, email, password, is_company):
        self.name = name
        self.document = document
        self.telephone = telephone
        self.email = email
        self.password = password
        self.is_company = is_company
        self.user_lock = threading.Lock()
        self.date_created_user = datetime.datetime.now()
        self.banks_with_account
    
    def get_json(self):
        self.user_lock.acquire()
        auxJson = {
            'name': self.name,
            'document': self.document,
            'telephone': self.telephone,
            'email': self.email,
            'is_company': self.is_company
        }
        self.user_lock.release()
        return auxJson
    

    def change_email(self, new_email):
        self.user_lock.acquire()
        if(self.email == new_email):
            self.user_lock.release()
            return 0 #the new email is same the old email
        else:
            self.email = new_email
            self.user_lock.release()
            return 1 #email changed
        
    
    def change_telephone(self, new_telephone):
        self.user_lock.acquire()
        if(self.telephone == new_telephone):
            self.user_lock.release()
            return 0 #the new telephone is same the old telephone
        else:
            self.telephone = new_telephone
            self.user_lock.release()
            return 1 #telephone changed
        
    
    def change_password(self, old_password, new_password):
        self.user_lock.acquire()
        if(cryptography_password(old_password) != self.password ):
            self.user_lock.release()
            return 0, "old password not match"
        elif(cryptography_password(new_password) == self.password):
            self.user_lock.release()
            return 0, "new password is equal as the previous"
        else:
            self.password = cryptography_password(new_password)
            self.user_lock.release()
            return 1, "password changed with success"
    
    
    def get_client_age_in_bank(self):
        self.user_lock.acquire()
        date_created_user = self.date_created_user
        self.user_lock.release()
        diference = datetime.datetime.now() - date_created_user
        days_user_in_bank = diference.days
        return days_user_in_bank
    
    
def cryptography_password(password):
    encrypted_password = sha512(password.encode()).digest()
    return encrypted_password        
        