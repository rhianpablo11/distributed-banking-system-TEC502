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
    pass
    
@app.route('/account/user/update-profile/change/telephone', methods=['PATCH'])


@app.route('/account/user/update-profile/change/email', methods=['PATCH'])


@app.route('/account/user/update-profile/change/password', methods=['PATCH'])



app.run("0.0.0.0", 50505, debug=False, threaded=True)
