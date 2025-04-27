import requests
import threading
from Run_Code import Run
from Run_Code1 import Run1
from Run_Code2 import Run2
from Run_Code3 import Run3
from Run_Code4 import Run4


id = 0
key = ""
ref_token = ""


def start(thresh, limit, blnc, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10):

    def get_token():
        url = "https://api.tdameritrade.com/v1/oauth2/token"

        params = {}
        params.update({'grant_type': 'refresh_token'})
        params.update({'refresh_token': ref_token})
        params.update({'client_id': key})

        return requests.post(url, data=params, timeout=60).json()

    # Use if refresh token expires
    def refresh_token():
        url = "https://api.tdameritrade.com/v1/oauth2/token"

        params = {}
        params.update({'grant_type': 'refresh_token'})
        params.update({'refresh_token': ref_token})
        params.update({'access_type': 'offline'})
        params.update({'client_id': key})

        return requests.post(url, data=params, timeout=60).json()

    def get_account(id, token):
        url = 'https://api.tdameritrade.com/v1/accounts/{}'.format(id)

        params = {}
        params.update({'Authorization': 'Bearer {}'.format(token)})
        return requests.get(url, headers=params, timeout=60).json()

    def run_M1():
        Run(lock, 0, token, trade_balance, thresh, limit, m1)

    def run_M2():
        Run(lock, 1, token, trade_balance, thresh, limit, m2)

    def run_M3():
        Run1(lock1, 2, token, trade_balance, thresh, limit, m3)

    def run_M4():
        Run1(lock1, 3, token, trade_balance, thresh, limit, m4)

    def run_M5():
        Run2(lock2, 4, token, trade_balance, thresh, limit, m5)

    def run_M6():
        Run2(lock2, 5, token, trade_balance, thresh, limit, m6)

    def run_M7():
        Run3(lock3, 6, token, trade_balance, thresh, limit, m7)

    def run_M8():
        Run3(lock3, 7, token, trade_balance, thresh, limit, m8)

    def run_M9():
        Run4(lock4, 8, token, trade_balance, thresh, limit, m9)

    def run_M10():
        Run4(lock4, 9, token, trade_balance, thresh, limit, m10)

    token = get_token()
    token = token["access_token"]
    print(token)
    account = get_account(id, token)
    Balance = account["securitiesAccount"]["currentBalances"]["cashAvailableForTrading"]
    blnc.set("Available Balance: " + str(Balance))
    print("Current Balance: " + str(Balance))
    trade_balance = Balance * 0.10

    lock = threading.Lock()
    lock1 = threading.Lock()
    lock2 = threading.Lock()
    lock3 = threading.Lock()
    lock4 = threading.Lock()
    m1_thread = threading.Thread(target=run_M1, daemon=True)
    m2_thread = threading.Thread(target=run_M2, daemon=True)
    m3_thread = threading.Thread(target=run_M3, daemon=True)
    m4_thread = threading.Thread(target=run_M4, daemon=True)
    m5_thread = threading.Thread(target=run_M5, daemon=True)
    m6_thread = threading.Thread(target=run_M6, daemon=True)
    m7_thread = threading.Thread(target=run_M7, daemon=True)
    m8_thread = threading.Thread(target=run_M8, daemon=True)
    m9_thread = threading.Thread(target=run_M9, daemon=True)
    m10_thread = threading.Thread(target=run_M10, daemon=True)
    m1_thread.start()
    m2_thread.start()
    m3_thread.start()
    m4_thread.start()
    m5_thread.start()
    m6_thread.start()
    m7_thread.start()
    m8_thread.start()
    m9_thread.start()
    m10_thread.start()
    m1_thread.join()
    m2_thread.join()
    m3_thread.join()
    m4_thread.join()
    m5_thread.join()
    m6_thread.join()
    m7_thread.join()
    m8_thread.join()
    m9_thread.join()
    m10_thread.join()
