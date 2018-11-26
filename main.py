from flask import Flask, jsonify
from pythonzimbra.communication import Communication
from pythonzimbra.tools import auth
from bitmath import *
import pythonzimbra.tools
import os
import ConfigParser

app = Flask(__name__)

ZIMBRA_URL = ''
ZIMBRA_USER = ''
ZIMBRA_PASSWORD = ''

def set_config_from_file():
    global ZIMBRA_URL, ZIMBRA_USER, ZIMBRA_PASSWORD

    if os.path.isfile(os.getcwd() + '/' + 'service.conf'):
        config = ConfigParser.ConfigParser()
        config.read('service.conf')
        ZIMBRA_URL = config.get('zimbra', 'zimbra_url')
        ZIMBRA_USER = config.get('zimbra', 'zimbra_user')
        ZIMBRA_PASSWORD = config.get('zimbra', 'zimbra_password')

def set_config_from_env():
    global ZIMBRA_URL, ZIMBRA_USER, ZIMBRA_PASSWORD
    if os.getenv('ZIMBRA_URL'):
        ZIMBRA_URL = os.getenv('ZIMBRA_URL')
    if os.getenv('ZIMBRA_USER'):
        ZIMBRA_USER = os.getenv('ZIMBRA_USER')
    if os.getenv('ZIMBRA_PASSWORD'):
        ZIMBRA_PASSWORD = os.getenv('ZIMBRA_PASSWORD')

def update_conf():
    set_config_from_file()
    set_config_from_env()

def get_token():
    return auth.authenticate(ZIMBRA_URL, ZIMBRA_USER, ZIMBRA_PASSWORD, admin_auth=True)

@app.route("/users", methods=['GET'])
def getUsuarios():
    update_conf()

    # TODO: check if server is reachable before communication
    usr_token = get_token()

    if not usr_token:
        print("[ERROR] Could not get Token, wrong username or password.")
        return "404"
    else:
        comm = Communication(ZIMBRA_URL)
        info_request = comm.gen_request(token=usr_token)
        info_request.add_request(
            'GetAllAccountsRequest',
            {},
            "urn:zimbraAdmin",
        )
        info_response = comm.send_request(info_request)

        res_dict = { "data": {}}
        i = 0

        for entry in info_response.get_response()['GetAllAccountsResponse']['account']:
            res_dict["data"][i] = {
                "id": entry["id"],
                "name": entry["name"]
                }
            i += 1

        return jsonify(res_dict)

@app.route("/users/quota", methods=['GET'])
def getUserQuota():
    update_conf()

    usr_token = get_token()

    if not usr_token:
        print("[ERROR] Could not get Token, wrong username or password.")
        return "404"
    else:
        comm = Communication(ZIMBRA_URL)
        info_request = comm.gen_request(token=usr_token)
        info_request.add_request(
            'GetQuotaUsageRequest',
            {},
            "urn:zimbraAdmin",
        )
        info_response = comm.send_request(info_request)

        res_dict = { "data": {}}
        i = 0
        for entry in info_response.get_response()['GetQuotaUsageResponse']['account']:
            res_dict["data"][i] = {
                "id": entry["id"],
                "name": entry["name"],
                "used": Byte(entry["used"]).best_prefix().format("{value:.2f} {unit}"),
                "limit": Byte(entry["limit"]).best_prefix().format("{value:.2f} {unit}")
            }
            i += 1
        print res_dict
        return jsonify(res_dict)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
