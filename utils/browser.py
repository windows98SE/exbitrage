# -*- coding: utf-8 -*-

import requests
import requests.utils
import requests.cookies

import urllib3
urllib3.disable_warnings()


class Browser:
    def __init__(self, **kwargs):
        self.session = requests.Session()

        self._useragent = kwargs.get('user_agent', self._user_agent())
        self._timeout = kwargs.get('timeout', 5)
        self._debug = kwargs.get('debug', False)

    def build_requests(self, **kwargs):
        if self._timeout:
            kwargs['timeout'] = self._timeout

        if self._debug:
            kwargs['verify'] = False
            kwargs['proxies'] = {
                'http': 'http://127.0.0.1:8080',
                'https': 'http://127.0.0.1:8080'
            }

        if 'headers' in kwargs:
            if 'User-Agent' not in kwargs['headers']:
                kwargs['headers'].update({'User-Agent': self._useragent})
        else:
            kwargs['headers'] = {'User-Agent': self._useragent}

        return kwargs

    def get(self, **kwargs):
        payload = self.build_requests(**kwargs)
        return self._response(self.session.get(**payload))

    def post(self, **kwargs):
        payload = self.build_requests(**kwargs)
        return self._response(self.session.post(**payload))

    def _response(self, resp):
        resp.encoding = resp.apparent_encoding
        if self._debug:
            print('response.text: {}'.format(resp.text))
        return resp

    @staticmethod
    def _user_agent():
        return ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/79.0.3945.79 Safari/537.36')
