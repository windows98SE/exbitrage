
from decimal import Decimal


def format_float(f):
    d = Decimal(str(f))
    s = d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()
    return str(s)
