from flask_cors import CORS
from flask import *


@app.route('/verify-conection', methods=['GET'])
def conectionTest():
    return "ok", 200


@app.route("/search-account", methods=['POST'])
def searchClient():
    dataReceived = request.json
    if(dataReceived['cpfCNPJ1'] in accounts):
        accounts[dataReceived['cpfCNPJ1']].addBankToList(dataReceived['bankName'])
        return 'user in the bank', 200
    else:
        return 'user not registed in the bank', 404


@app.route('/bank', methods=['GET'])
def getNameBank():
    dataSend = {
        "nameBank": "bank"
    }
    response = make_response(jsonify(dataSend))
    return response, 200


@app.route('/account/transaction/pix/infos', methods=['POST'])
def getInfosForMakePix():
    data =  request.json
    if(data["bankID"] == "1" or data["bankID"] == "2" or data["bankID"] == "3" or data["bankID"] == "4" or data["bankID"] == "5"):
        url = listBanksConsortium[data["bankID"]][0]+"/account/pix"
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
            return "Account not found",400              
    else:
        return "Bank invalid", 404
    




app.run("0.0.0.0", 50505, debug=False, threaded=True)
