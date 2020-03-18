# -*- coding: utf-8 -*-

from time import time


def nonce():
    return str(int(time()))
