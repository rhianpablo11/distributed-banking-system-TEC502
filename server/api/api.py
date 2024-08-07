from flask_cors import CORS
from flask import *
from storage import accounts_storage

app = Flask(__name__)
CORS(app)
app.run("0.0.0.0", 50505, debug=False, threaded=True)

@app.route("/search-account/<int:account_number>", methods=['POST'])
def search_account(account_number):
    accounts_storage.find_account_by_number_account(account_number)
    make_response(jsonify(accounts_storage.find_account_by_number_account(account_number).get_json_basic_data()))


@app.route('/bank', methods=['GET'])
def getNameBank():
    pass

@app.route('/account/transaction/pix/infos', methods=['POST'])
def getInfosForMakePix():
    pass
    
@app.route('/account/user/update-profile/change/telephone', methods=['PATCH'])


@app.route('/account/user/update-profile/change/email', methods=['PATCH'])


@app.route('/account/user/update-profile/change/password', methods=['PATCH'])
def getInfosForMakePix():
    pass