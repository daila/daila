
'''
Field inversion for BBE251 elliptic curve
'''

def mul(a, b, m):
    c = 0
    while b:
        if b & 1:
            c ^= a
        a <<= 1
        b >>= 1
    if c.bit_length() < m.bit_length():
        return c
    n = m.bit_length() - 1
    return (c & ((1 << n) - 1)) ^ mul(c >> n, m & ((1 << n) - 1), m)


def exp(x, n, m):
    xx = 1
    while n:
        if n & 1:
            xx = mul(xx, x, m)
        x = mul(x, x, m)
        n >>= 1
    return xx


def inv(x, m):
    return exp(x, 2**(m.bit_length() - 1) - 2, m)


def params_1():
    m = 2**8 + 2**4 + 2**3 + 2**1 + 1
    a = 2**8 + 2**0
    b = 2**7 + 2**6 + 2**5 + 2**4 + 2**3 + 2**2 + 2**0
    return a, b, m


def params_bbe251():
    m = 2**251 + 2**7 + 2**4 + 2**2 + 1
    d = 2**57 + 2**54 + 2**44 + 1
    return m, d


