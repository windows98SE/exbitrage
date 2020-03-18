# -*- coding: utf-8 -*-

import hashlib
import hmac
import os

from utils.browser import Browser
from utils.gmt import nonce


class SATANG:
    """
    Official Documentation for Satang Pro APIs
    https://docs.satang.pro

    ~~~ wtf(p)!!!, where to find (python)!!!
    """
    def __init__(self, debug=False):
        self._api = 'https://api.satang.pro/api'
        self._uid = os.getenv('SATANG_USER_ID', '')
        self._key = os.getenv('SATANG_API_KEY', '')
        self._secret = os.getenv('SATANG_API_SECRET', '').encode('utf-8')

        self._debug = debug
        self._browser = Browser(debug=self._debug)

    ##########
    # --- public api ---
    # Get ticker information.
    def get_bids_asks(self, sym='btc_thb'):
        """
        :return: {
         'asks': [[rate, amount], [174629, 0.00010107], ...],
         'bids': [[rate, amount], [174629, 0.00010107], ...]
        }
        """
        payload = {'url': self._api + f'/orders/?pair={sym.lower()}'}
        return self._resp_order(self._resp(self._browser.get(**payload)))

    ##########
    # --- private api ---
    # User
    def user(self):
        payload = {
            'url': self._api + f'/users/:{self._uid}',
            'headers': self._build_headers()
        }
        return self._resp(self._browser.get(**payload))

    # Create a buy order.
    def buy(self, pair, price, amount, typ='limit'):
        data = {
            'pair': pair.lower(),
            'price': price,
            'amount': amount,
            'side': 'buy',
            'type': ('limit' if typ == 'limit' else 'market'),
            'nonce': nonce()
        }
        print(data)
        return self._create_orders(**data)

    # Create a sell order.
    def sell(self, pair, price, amount, typ='limit'):
        data = {
            'pair': pair.lower(),
            'price': price,
            'amount': amount,
            'side': 'sell',
            'type': ('limit' if typ == 'limit' else 'market'),
            'nonce': nonce()
        }
        return self._create_orders(**data)

    def _create_orders(self, **kwargs):
        data = self._concatenate_params(**kwargs)
        payload = {
            'url': self._api + '/orders/',
            'headers': self._build_headers(data),
            'data': data
        }
        return self._resp(self._browser.post(**payload))

    ##########
    # utility
    def _build_headers(self, s=''):
        return {
            'Authorization': 'TDAX-API ' + self._key,
            'Signature': hmac.new(self._secret, s.encode('utf-8'), hashlib.sha512).hexdigest(),
        }

    def _resp(self, resp):
        if resp.status_code == 200:
            return resp.json()
        if self._debug:  # catch error !?
            raise Exception(resp)

    @staticmethod
    def _resp_order(o):
        return {
            'bids': [[_['price'], _['amount']] for _ in o['bid']],
            'asks': [[_['price'], _['amount']] for _ in o['ask']]
        }

    @staticmethod
    def _concatenate_params(**p):
        print(p)
        return'&'.join(sorted(['{}={}'.format(_, p[_]) for _ in p])) if p else ''


if __name__ == '__main__':
    satang = SATANG(debug=True)
    # satang = SATANG()

    # bids_asks = satang.get_bids_asks()
    #
    # print(bids_asks)
    #
    # # # -- private api -- #
    # user = satang.user()
    # print(user)

    b = satang.buy('btc_thb', 10000, 0.1)
    print(b)
