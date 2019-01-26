
from crypto import m, reduction_poly_bits, fe_sq, fe_rand

def test_fe_sq():
    from crypto import fe_mul
    return all(
        fe_sq(x) == fe_mul(x,x) for x in (fe_rand() for i in range(100))
    )


def test_fe_sqrt():
    from crypto import fe_sqrt
    return all(
        fe_sq(fe_sqrt(x)) == x for x in (fe_rand() for i in range(100))
    )


def test_fe_inv():
    from crypto import fe_mul, fe_inv
    return all(
        fe_mul(x, fe_inv(x)) == 1 for x in (fe_rand() for i in range(100))
    )

def test_trace_bits():
    from crypto import trace_bits
    x = [set() for i in range(m)]
    a = [{i} for i in range(m)]
    for i in range(m):
        x = _xor_bits(x, a)
        a = _sq_bits(a)
    bits = set()
    for i in x:
        bits ^= i
    return bits == set(trace_bits)


def test_trace():
    from crypto import trace
    def tr(x):
        a = 0
        for i in range(m):
            a ^= x
            x = fe_sq(x)
        x = 0
        for i in range(m):
            x ^= a % 2
            a >> 1
        return x
    return all(tr(x) == trace(x) for x in (fe_rand() for i in range(100)))


def test_half_trace():
    from crypto import half_trace
    def htr(x):
        a = 0
        for i in range((m-1)//2 + 1):
            a ^= x
            x = fe_sq(x)
            x = fe_sq(x)
        return a
    return all(
        htr(x) == half_trace(x) for x in (fe_rand() for i in range(100))
    )


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
        for n in reduction_poly_bits:
            x = _xor_bits(x, _shl_bits(a, n))
    return x
