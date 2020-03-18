
from exchange.bitkub import BITKUB
from exchange.satang import SATANG


class EXBITRAGE:
    def __init__(self, ex_a, ex_b):
        self._ex_a = ex_a
        self._ex_b = ex_b

    def do_it_later(self):
        pass


if __name__ == '__main__':
    bitkub = BITKUB()
    satang = SATANG()

    run = EXBITRAGE(bitkub, satang)
