import threading
import os
import sys
from time import sleep
from flask import *
import json
from datetime import *
from flask_cors import CORS
from clientModel import Client
from transactionModel import Transaction
import requests

global clients
clients = {}
clientsLock = threading.Lock()


IP = '0.0.0.0'
global bankName
bankName = "elevenBank"

global hashMapBanks
hashMapBanks = {
    "1": "localhost:8081"
}

global accountNumbers
accountNumbers = 2;

app = Flask(__name__)
CORS(app)


#função geradora de numero de conta conta
def createAccountNumber():
    global accountNumbers
    accountNumber = (accountNumbers**10+12*accountNumbers+(6*(accountNumbers**3)))/2
    accountNumbers +=2
    return accountNumber


@app.route('/bank', methods=['GET'])
def getNameBank():
    return bankName, 200


@app.route('/clients', methods=['GET'])
def getClientsList():
    
    clientsList = []
    if(len(clients) >0):
        for client in clients:
            clientsList.append(clients[client].jsonComplet())
    print(clientsList)
    print(clientsLock)
    response = make_response(jsonify(clientsList))
    response.headers['Cache-Control'] = 'private, max-age=1'

    return response


@app.route('/client/create', methods=['POST'])
def createClient():
    global clients
    data = request.json
    clientsLock.acquire()
    #verificar se tem todos os elementos
    if(data["name1"]  and data["cpfCNPJ1"] and data["name2"] and data["cpfCNPJ2"] and data["email"] and data["password"] and data["isFisicAccount"] and data["isJoinetAccount"] and data["telephone"]):
        if(data["cpfCNPJ1"] in clients):
            clientsLock.release()
            return "user already in system", 409
        else:
            clients[data["cpfCNPJ1"]] = Client(
                                            name1= data["name1"],
                                            cpfCNPJ1= data["cpfCNPJ1"],
                                            name2= data["name2"],
                                            cpfCNPJ2= data["cpfCNPJ2"],
                                            email=data["email"],
                                            password= data["password"],
                                            isFisicAccount= data["isFisicAccount"],
                                            isJoinetAccount=data["isJoinetAccount"],
                                            accountNumber= createAccountNumber(),
                                            telephone= data["telephone"],
                                            bank=bankName,
                                            balance="0",
                                            blockedBalance="0"    )
            
            response = make_response(jsonify(clients[data["cpfCNPJ1"]].jsonComplet()))
            clientsLock.release()
            return response, 201
    else:
        clientsLock.release()
        return "infos received not are complete", 406


"""
Função para procurar um cliente, e retornar dados basicos deste cliente
Esses dados são retornados para quem quer fazer o pix
"""
@app.route('/client/pix', methods=['GET'])
def getClientPixInfo(): #fazer o retorno de informações basicas para apresentar na hora do pix
    data = request.json
    if(len(clients) >0):
        for client in clients:
            print(clients[client].email)
            if(data["keyPix"] == clients[client].keyPix):
                print(clients[client].infoBasic())
                response = make_response(jsonify(clients[client].infoBasic()))
                return response
        else:
            return "client not found", 404
    else:
        return "client not found", 404
    

"""
Essa função realiza a operação de ativar a chave pix do cliente
"""
@app.route('/client/keypix', methods=["PATCH"])
def changeStatusKeyPix():
    data = request.json
    if(len(clients) >0):
        for client in clients:
            if(data["cpfCNPJ1"] == client):
                clients[client].setKeyPix(data["active"])
                return clients[client].keyPix, 201
        else:
            return "client not found", 404 
    else:
        return "client not found", 404


"""
Função para receber um dinheiro provindo de deposito comum
"""
@app.route('/client/deposit', methods=["PATCH"])
def depositMoney():
    data =  request.json
    if(len(clients) >0):
        for client in clients:
            if(data["cpfCNPJ1"] == client):
                if(clients[client].receiveDeposit(data["value"])):
                    return "money received with sucess", 201
                else:
                    return "error in complet transaction", 403
        else:
            return "client not found", 404 
    else:
        return "client not found", 404


'''
Função para realizar o login do usuario
'''
@app.route('/client/login', methods=['GET'])
def loginClient():
    data =  request.json
    if(len(clients) >0):
        for client in clients:
            if(clients[client].email == data["email"]):
                if(clients[client].password == data["password"]):
                    print(clients[client].jsonComplet())
                    response = make_response(jsonify(clients[client].jsonComplet()))
                    return response, 200
                else:
                    return "password incorrect", 401
        else:
            return "client not found", 404 
    else:
        return "client not found", 404    



'''
Função para requisitar ao outro banco as informações do pix daquele usuario
'''
@app.route('/client/transaction/pix/infos', methods=['GET'])
def getInfosForMakePix():
    data =  request.json
    if(data["bankID"] == "1"):
        url = "http://"+hashMapBanks[data["bankID"]]+"/client/pix"
        keyPix = {
            "keyPix": str(data["keyPix"])
        }
        infoReceived = requests.get(url,json=keyPix)
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
Função para poder enviar o dinheiro via pix para outro cliente
'''
@app.route('/client/transactions/pix/send', methods=['POST'])
def sendMoneyPix():
    data =  request.json

    if(data["bankID"] == "1"):
        url = "http://"+hashMapBanks[data["bankID"]]+"/client/transactions/pix/receive"
        print(url)
        addMoney = clients[data["cpfCNPJ1"]].sendPix(data["value"], url, data["keyPix"], data["nameReceptor"])
        print(addMoney)
        if(addMoney[1]):
            return "money send with sucess", 200
        elif(addMoney[0]=="error in transaction"):
            return "error in transaction", 406
        else:
            return "error, key is same of client", 403
        
    else:
        return "Bank invalid",400



'''
Função para receber dinheiro via pix
'''
@app.route('/client/transactions/pix/receive', methods=['PATCH'])
def receiveMoneyPix():
    data = request.json
    if(len(clients) >0):
        #SE A CHAVE PIX SE MANTER O CPF, NAO PRECISA PERCORRER O FOR
        for client in clients:
            if(data["keyPix"] == clients[client].keyPix):
                if(clients[client].receivePix(data["value"], data["bankName"], data["sender"])):
                    return "money received with sucess", 200
                else:
                    return "error in transaction", 403
        else:
            return "client not found", 404 
    else:
        return "client not found", 404

app.run(IP, 8082, debug=False, threaded=True)

