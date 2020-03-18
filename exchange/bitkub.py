# -*- coding: utf-8 -*-

import hashlib
import hmac
import json
import os

from utils.browser import Browser
from utils.formatter import format_float
from utils.gmt import nonce


class BITKUB:
    """
    Official Documentation for Bitkub APIs
    https://github.com/bitkub/bitkub-official-api-docs
    """
    def __init__(self, debug=False):
        self._api = 'https://api.bitkub.com/api'
        self._key = os.getenv('BITKUB_API_KEY', '')
        self._secret = os.getenv('BITKUB_API_SECRET', '').encode()

        self._debug = debug
        self._browser = Browser(debug=self._debug)

    ##########
    # --- public api ---
    # Get ticker information.
    def ticker(self, sym=''):
        sym = '' if sym == '' else f'?sym={sym.upper()}'
        payload = {'url': self._api + f'/market/ticker{sym}'}
        return self._resp(self._browser.get(**payload))

    # List open (bids/asks) orders.
    def get_bids_asks(self, sym='THB_BTC', lmt=10):
        """
        :return: {
         'asks': [[rate, amount], [174629, 0.00010107], ...],
         'bids': [[rate, amount], [174629, 0.00010107], ...]
        }
        """
        payload = {'url': self._api + f'/market/depth?sym={sym.upper()}&lmt={lmt}'}
        return self._resp(self._browser.get(**payload))

    # List open buy(bids) orders.
    def get_bids(self, sym='THB_BTC', lmt=10):
        """
        :return: [[rate, volume, amount], [174629, 17.65, 0.00010107], ...]
        """
        payload = {'url': self._api + f'/market/bids?sym={sym.upper()}&lmt={lmt}'}
        return self._resp_order(self._resp(self._browser.get(**payload)))

    # List open sell(asks) orders.
    def get_asks(self, sym='THB_BTC', lmt=10):
        """
        :return: [[rate, volume, amount], [175500, 928.14, 0.00528859], ...]
        """
        payload = {'url': self._api + f'/market/asks?sym={sym.upper()}&lmt={lmt}'}
        return self._resp_order(self._resp(self._browser.get(**payload)))

    ##########
    # --- private api ---
    # Get balances info
    def balance(self):
        payload = {
            'url': self._api + '/market/balances',
            'headers': self._build_headers(),
            'data': self._build_sign({})
        }
        return self._resp(self._browser.post(**payload))

    # Create a sell order.
    def sell(self, **kwargs):
        """
        :param kwargs: sym, amt, rat, typ
        """
        payload = {
            'url': self._api + '/market/place-ask',
            'headers': self._build_headers(),
            'data': self._build_sign(self._data_rules(**kwargs))
        }
        return self._resp(self._browser.post(**payload))

    # Create a buy order.
    def buy(self, **kwargs):
        """
        :param kwargs: sym, amt, rat, typ
        """
        payload = {
            'url': self._api + '/market/place-bid',
            'headers': self._build_headers(),
            'data': self._build_sign(self._data_rules(**kwargs))
        }
        return self._resp(self._browser.post(**payload))

    ##########
    # utility
    def _build_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-APIKEY': self._key,
        }

    def _build_sign(self, data):
        data['ts'] = nonce()
        data['sig'] = hmac.new(self._secret, self._json_encode(data).encode(), hashlib.sha256).hexdigest()
        return self._json_encode(data)

    @staticmethod
    def _data_rules(**kwargs):
        params = {}
        if 'sym' in kwargs:  # symbol is upper case
            params['sym'] = kwargs['sym'].upper()
        if 'amt' in kwargs:  # 0.10000000 is invalid, 0.1 is ok
            params['amt'] = format_float(kwargs['amt'])
        if 'rat' in kwargs:  # (e.g 1000.00 is invalid, 1000 is ok)
            params['rat'] = format_float(kwargs['rat'])
        if 'typ' in kwargs:  # limit or market
            params['typ'] = ('market' if kwargs['typ'] == 'market' else 'limit')
        return params

    def _resp(self, resp):
        if resp.status_code == 200:
            if resp.json().get('error') == 0:
                return resp.json()['result']
            return resp.json()
        if self._debug:  # catch error !?
            raise Exception(resp)

    @staticmethod
    def _resp_order(o):
        # idx, timestamp, volume, rate, amount
        return [[r, v, a] for i, t, v, r, a in o]

    @staticmethod
    def _json_encode(data):
        return json.dumps(data, separators=(',', ':'), sort_keys=True)


if __name__ == '__main__':
    bitkub = BITKUB()
    # bitkub = BITKUB(debug=True)

    ticker = bitkub.ticker()
    bids_asks = bitkub.get_bids_asks()
    bids = bitkub.get_bids('THB_BTC')
    asks = bitkub.get_asks('THB_ETH', 50)

    print(ticker)
    print(ticker['THB_BTC'])
    print(bids_asks)
    print(bids)
    print(asks)

    # # -- private api -- #
    balance = bitkub.balance()
    print(balance)
