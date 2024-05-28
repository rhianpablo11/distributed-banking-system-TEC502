import threading
import os
import sys
from flask import *
import json
from datetime import *
from flask_cors import CORS
from model import Client
import requests

global clients
clients = {}

IP = '0.0.0.0'
global bankName
bankName = "automobili Bank"

global hashMapBanks
hashMapBanks = {
    "1": "localhost:8082"
}

global accountNumbers
accountNumbers = 2;

app = Flask(__name__)
CORS(app)


#função geradora de numero de conta conta
def createAccountNumber():
    global accountNumbers
    accountNumber = accountNumbers**10+12*accountNumbers+(6*(accountNumbers**3))
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

    response = make_response(jsonify(clientsList))
    response.headers['Cache-Control'] = 'private, max-age=1'
    return response


@app.route('/client/create', methods=['POST'])
def createClient():
    global clients
    data = request.json
    #verificar se tem todos os elementos
    if(data["name1"]  and
       data["cpfCNPJ1"] and
       data["name2"] and
       data["cpfCNPJ2"] and
       data["email"] and
       data["password"] and
       data["isFisicAccount"] and
       data["isJoinetAccount"] and
       data["telephone"]):
        if(data["cpfCNPJ1"] in clients):
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
            print(clients[data["cpfCNPJ1"]].jsonComplet())
            response = make_response(jsonify(clients[data["cpfCNPJ1"]].jsonComplet()))
            return response, 201
    else:
        return "infos received not are complete", 406


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


#funcao de receber via deposito comum
@app.route('/client/deposit', methods=["PATCH"])
def depositMoney():
    data =  request.json
    if(len(clients) >0):
        for client in clients:
            if(data["cpfCNPJ1"] == client):
                oldBalance = clients[client].balance
                newBalance = float(oldBalance) + float(data["value"])
                clients[client].setBalance(newBalance)
                return "money received with sucess", 201
        else:
            return "client not found", 404 
    else:
        return "client not found", 404


@app.route('/client/login', methods=['GET'])
def loginClient():
    data =  request.json
    if(len(clients) >0):
        for client in clients:
            if(clients[client].email == data["email"]):
                if(clients[client].password == data["password"]):
                    response = make_response(jsonify(clients[client].jsonComplet()))
                    return response, 200
                else:
                    return "password incorrect", 401
        else:
            return "client not found", 404 
    else:
        return "client not found", 404    


@app.route('/client/transaction/pix/infos', methods=['GET'])
def getInfosForMakePix():
    data =  request.json
    if(data["bankID"] == 1):
        url = "http://"+hashMapBanks[data["bankID"]]+"/client/pix"
        keyPix = {
            "keyPix": data["keyPix"]
        }
        infoReceived = requests.get(url,params=jsonify(keyPix))
        if (infoReceived.status_code == 200):
            print(infoReceived.json())
            response = make_response(infoReceived.json())
            return response, 200
        else:
            print(infoReceived.status_code, infoReceived.text)
            return "Error in requisition",400              
    else:
        return "Bank invalid", 404

#metodo para enviar o dinheiro via pix
@app.route('/client/transactions/pix/send', methods=['POST'])
def sendMoneyPix():
    data =  request.json
    if(float(data["value"])<=float(clients[data["cpfCNPJ1"]].balance)):
        oldBalance = clients[data["cpfCNPJ1"]].balance
        newBalance = oldBalance - float(data["value"])
        clients[data["cpfCNPJ1"]].setBalance(newBalance)
        clients[data["cpfCNPJ1"]].setBlockedBalance(float(data["value"]))
        
        if(data["bankID"] == 1):
            url = "http://"+hashMapBanks[data["bankID"]]+"/client/transactions/pix/receive"
            datasForSend = {}
            datasForSend["keyPix"] = data["keyPix"]
            datasForSend["value"] = data["value"]
            datasForSend["sender"] = data["cpfCNPJ1"]
            infoReceived = requests.get(url,params=datasForSend)
            

            if (infoReceived.status_code == 200): #achou o cliente no outro banco
                print(infoReceived.json())
                clients[data["cpfCNPJ1"]].setBlockedBalance((-1)*(float(data["value"])))
            else: #nao encontrou o cliente no outro banco
                print(infoReceived.status_code, infoReceived.text)
                clients[data["cpfCNPJ1"]].setBlockedBalance((-1)*(float(data["value"])))
                oldBalance = clients[data["cpfCNPJ1"]].balance
                newBalance = oldBalance + float(data["value"])
                clients[data["cpfCNPJ1"]].setBalance(newBalance)
                return "Error in requisition",400

#metodo para ele receber o dinheiro via pix
@app.route('/client/transactions/pix/receive', methods=['PATCH'])
def receiveMoneyPix():
    data = request.json
    if(len(clients) >0):
        for client in clients:
            if(data["keyPix"] == clients[client].keyPix):
                oldBalance = clients[client].balance
                newBalance = float(oldBalance) + float(data["value"])
                clients[client].setBalance(newBalance)
                return "money received with sucess", 200
        else:
            return "client not found", 404 
    else:
        return "client not found", 404

app.run(IP, 8081, debug=False)

