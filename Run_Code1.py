import requests
import time
import json
import math
from security import safe_requests

key = "OPE9A7YLKQXGTWXJAFLIAEBIEXT4NXWU"
id = 270508762


def Run1(Lock, index, token, balance, t, l, m):
    def get_movers(d, c):
        url = "https://api.tdameritrade.com/v1/marketdata/$COMPX/movers"

        params = {}
        params.update({'apikey': key})
        params.update({'direction': d})
        params.update({'change': c})

        movers = safe_requests.get(url, params=params).json()
        Movers = {}

        if movers[index]["last"] < l:
            Movers[movers[index]["symbol"]] = movers[index]["last"]
            return Movers
        else:
            return 0

    def get_price(s):
        url = 'https://api.tdameritrade.com/v1/marketdata/{}/quotes'.format(s)

        params = {}
        params.update({'apikey': key})

        price = safe_requests.get(url, params=params).json()
        price = price[s]["lastPrice"]
        return price

    def handle_trade(ID, symbol, quantity, buy_price):
        url = "https://api.tdameritrade.com/v1/accounts/{}/orders".format(ID)
        Type = "Sell"

        params = {
            "orderType": "MARKET",
            "session": "NORMAL",
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": "{}".format(Type),
                    "quantity": "{}".format(quantity),
                    "instrument": {
                        "symbol": "{}".format(symbol),
                        "assetType": "EQUITY"
                    }
                }
            ]
        }

        header = {}
        header.update({"Authorization": "Bearer {}".format(token)})
        header.update({"Content-Type": "application/json"})

        while True:
            Lock.acquire()
            price1 = get_price(symbol)
            Lock.release()
            diff = round(price1 - buy_price, 2)
            print(str(symbol) + " " + str(buy_price) + " " + str(price1) + " " + str(diff))
            if diff >= t:
                Lock.acquire()
                data = requests.post(url, data=json.dumps(params), headers=header)
                Lock.release()
                print(data.status_code)
                if data.status_code == 201:
                    print(str(index) + " Sold " + str(quantity) + " shares of " + symbol)
                break

    def place_order(ID, symbol, quantity):
        url = "https://api.tdameritrade.com/v1/accounts/{}/orders".format(ID)
        Type = "Buy"

        params = {
            "orderType": "MARKET",
            "session": "NORMAL",
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": "{}".format(Type),
                    "quantity": "{}".format(quantity),
                    "instrument": {
                        "symbol": "{}".format(symbol),
                        "assetType": "EQUITY"
                    }
                }
            ]
        }

        header = {}
        header.update({"Authorization": "Bearer {}".format(token)})
        header.update({"Content-Type": "application/json"})

        Lock.acquire()
        data = requests.post(url, data=json.dumps(params), headers=header)
        time.sleep(1)
        bp = get_price(symbol)
        Lock.release()
        print(data.status_code)
        if data.status_code == 201:
            print(str(index) + " Bought " + str(quantity) + " shares of " + symbol)
            handle_trade(ID, symbol, quantity, bp)

    while True:
        Lock.acquire()
        movers = get_movers('up', 'percent')
        time.sleep(2)
        Lock.release()
        if movers != 0:
            keys = list(movers.keys())
            sym = keys[0]
            price = movers.get(sym)
            Lock.acquire()
            price1 = get_price(sym)
            m.set("M" + str(index + 1) + ": " + sym + " ,Price: " + str(price1))
            Lock.release()
            diff = round(price - price1, 2)
            print(str(index + 1) + " " + str(sym) + " " + str(price) + " " + str(price1) + " " + str(diff))
            if diff == t:
                q = math.floor(balance/price1)
                if q < 1:
                    print("Balance low for placing this order: " + str(balance))
                else:
                    place_order(id, sym, q)
                break
        else:
            print(str(index + 1) + " Movers price greater than $15. Check again after 1 min")
            m.set("M" + str(index + 1) + ": Price > limit")
            time.sleep(60)
