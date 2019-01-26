
from crypto import m, reduction_poly


def test_trace_bits():
    from crypto import trace_bits
    x = [[] for i in range(m)]
    a = [[i] for i in range(m)]
    for i in range(m):
        x = _add_bits(x, a)
        a = _sq_bits(a)
    bits = set()
    for i in x:
        bits ^= i
    assert bits == set(trace_bits)


def test_trace():
    from crypto import trace, fe_rand
    def tr(x):
        a = 0
        for i in range(m):
            a ^= x
            x = _fe_sq(x)
        x = 0
        for i in range(m):
            x ^= a % 2
            a >> 1
        return x
    assert all(tr(x) == trace(x) for x in (fe_rand() for i in range(100)))


def test_half_trace():
    pass


def _shl_bits(a, n):
    return [set() for i in range(n)] + a


def _xor_bits(a, b):
    n = max(len(a), len(b))
    a = a + [set() for i in range(n - len(a))]
    b = b + [set() for i in range(n - len(b))]
    return [i ^ j for i, j in zip(a, b)]


def _sq_bits(a):
    x = []
    for i in range(m-1):
        x.extend([a[i], set()])
    x.append(a[-1])
    for i in range(2):
        x, a = x[:m], x[m:]
        for n in reduction_poly:
            x = _xor_bits(x, _shl_bits(a, n))
    return x


def _fe_sq(x):
    a = 0
    for i in range(m):
        a |= (x & (1 << i)) << 1
    for i in range(2):
        x, a = a >> m, a % (2**m)
        for bit in reduction_poly:
            a ^= x << bit
    return a

