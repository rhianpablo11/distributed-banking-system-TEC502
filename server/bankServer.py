
import threading
global accountNumbers
import os
import sys
from time import sleep
from flask import *
import json
from datetime import *
from flask_cors import CORS
from accountModel import Account
from transactionModel import Transaction
import requests
from utils import *
import random

global accounts
accounts = {}
accountsLock = threading.Lock()


IP = '0.0.0.0'
global bankName
bankName = "Eleven"

global hashMapBanks
hashMapBanks = {
    "1": "localhost:8082"
}

            


accountNumbers = GenerateNumberAccountBank

app = Flask(__name__)
CORS(app)





@app.route('/bank', methods=['GET'])
def getNameBank():
    dataSend = {
        "nameBank": bankName
    }
    response = make_response(jsonify(dataSend))
    return response, 200


@app.route('/accounts', methods=['GET'])
def getaccountsList():
    
    accountsList = []
    if(len(accounts) >0):
        for account in accounts:
            accountsList.append(accounts[account].jsonComplet())
    print(accountsList)
    print(accountsLock)
    response = make_response(jsonify(accountsList))
    response.headers['Cache-Control'] = 'private, max-age=1'

    return response


@app.route('/account/create', methods=['POST'])
def createaccount():
    global accounts
    data = request.json
    accountsLock.acquire()
    #verificar se tem todos os elementos
    if(data["name1"]  and data["cpfCNPJ1"] and data["name2"] and data["cpfCNPJ2"] and data["email"] and data["password"] and data["isFisicAccount"] and data["isJoinetAccount"] and data["telephone"]):
        if(data["cpfCNPJ1"] in accounts):
            accountsLock.release()
            return "user already in system", 409
        else:
            accounts[data["cpfCNPJ1"]] = Account(
                                            name1= data["name1"],
                                            cpfCNPJ1= data["cpfCNPJ1"],
                                            name2= data["name2"],
                                            cpfCNPJ2= data["cpfCNPJ2"],
                                            email=data["email"],
                                            password= cryptographyPassword(data["password"]),
                                            isFisicAccount= data["isFisicAccount"],
                                            isJoinetAccount=data["isJoinetAccount"],
                                            accountNumber= random.randint(1000, 9999),
                                            telephone= data["telephone"],
                                            bank=bankName,
                                            balance="0",
                                            blockedBalance="0",
                                            listBanks=[]    )
            
            response = make_response(jsonify(accounts[data["cpfCNPJ1"]].jsonComplet()))
            accountsLock.release()
            return response, 201
    else:
        accountsLock.release()
        return "infos received not are complete", 406


"""
Função para procurar um accounte, e retornar dados basicos deste accounte
Esses dados são retornados para quem quer fazer o pix
"""
@app.route('/account/pix', methods=['POST'])
def getaccountPixInfo(): #fazer o retorno de informações basicas para apresentar na hora do pix
    data = request.json
    if(len(accounts) >0):
        for account in accounts:
            print(accounts[account].email)
            if(data["keyPix"] == accounts[account].keyPix):
                print(accounts[account].infoBasic())
                response = make_response(jsonify(accounts[account].infoBasic()))
                return response
        else:
            return "account not found", 404
    else:
        return "account not found", 404
    

"""
Essa função realiza a operação de ativar a chave pix do accounte
"""
@app.route('/account/keypix', methods=["PATCH"])
def changeStatusKeyPix():
    data = request.json
    if(len(accounts) >0):
        for account in accounts:
            if(data["cpfCNPJ1"] == account):
                accounts[account].setKeyPix(data["active"])
                return accounts[account].keyPix, 201
        else:
            return "account not found", 404 
    else:
        return "account not found", 404


"""
Função para receber um dinheiro provindo de deposito comum
"""
@app.route('/account/deposit', methods=["PATCH"])
def depositMoney():
    data =  request.json
    if(len(accounts) >0):
        for account in accounts:
            if(data["cpfCNPJ1"] == account):
                if(accounts[account].receiveDeposit(data["value"])):
                    return "money received with sucess", 201
                else:
                    return "error in complet transaction", 403
        else:
            return "account not found", 404 
    else:
        return "account not found", 404


'''
Função para realizar o login do usuario
'''
@app.route('/account/login', methods=['POST'])
def loginaccount():
    data =  request.json
    if(len(accounts) >0):
        for account in accounts:
            if(accounts[account].email == data["email"]):
                if(accounts[account].password == cryptographyPassword(data["password"])):
                    response = make_response(jsonify(accounts[account].jsonComplet()))
                    return response, 200
                else:
                    return "password incorrect", 401
        else:
            return "account not found", 404 
    else:
        return "account not found", 404    

@app.route('/account/data/<int:accountNumber>', methods=['GET'])
def getInfoAboutAccount(accountNumber):
    if(len(accounts) >0):
        for account in accounts:
            if(accounts[account].accountNumber == accountNumber):
                response = make_response(jsonify(accounts[account].jsonComplet()))
                return response, 200
                
        else:
            return "account not found", 404 
    else:
        return "account not found", 404 

'''
Função para requisitar ao outro banco as informações do pix daquele usuario
'''
@app.route('/account/transaction/pix/infos', methods=['POST'])
def getInfosForMakePix():
    data =  request.json
    if(data["bankID"] == "1"):
        url = "http://"+hashMapBanks[data["bankID"]]+"/account/pix"
        keyPix = {
            "keyPix": str(data["keyPix"])
        }
        infoReceived = requests.post(url,json=keyPix)
        if (infoReceived.status_code == 200):
            print(infoReceived.json())
            response = make_response(infoReceived.json())
            return response, 200
        else:
            print(infoReceived.status_code, infoReceived.text)
            return "Error in requisition",400              
    else:
        return "Bank invalid", 404


'''
Função para poder enviar o dinheiro via pix para outro accounte
'''
@app.route('/account/transactions/pix/send', methods=['POST'])
def sendMoneyPix():
    data =  request.json

    if(data["bankID"] == "1"):
        url = "http://"+hashMapBanks[data["bankID"]]+"/account/transactions/pix/receive"
        print(url)
        addMoney = accounts[data["cpfCNPJ1"]].sendPix(data["value"], url, data["keyPix"], data["nameReceptor"])
        print(addMoney)
        if(addMoney[1]):
            return "money send with sucess", 200
        elif(addMoney[0]=="error in transaction"):
            return "error in transaction", 406
        else:
            return "error, key is same of account", 403
        
    else:
        return "Bank invalid",400



'''
Função para receber dinheiro via pix
'''
@app.route('/account/transactions/pix/receive', methods=['PATCH'])
def receiveMoneyPix():
    data = request.json
    if(len(accounts) >0):
        #SE A CHAVE PIX SE MANTER O CPF, NAO PRECISA PERCORRER O FOR
        for account in accounts:
            if(data["keyPix"] == accounts[account].keyPix):
                if(accounts[account].receivePix(data["value"], data["bankName"], data["sender"])):
                    return "money received with sucess", 200
                else:
                    return "error in transaction", 403
        else:
            return "account not found", 404 
    else:
        return "account not found", 404

app.run(IP, 8082, debug=False, threaded=True)

