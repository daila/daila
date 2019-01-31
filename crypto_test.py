
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


# def test_half_trace_bits():
#     def generate_bits():
#         x = [set() for i in range(m)]
#         a = [{i} for i in range(m)]
#         for i in range(0, m, 2):
#             x = _xor_bits(x, a)
#             a = _sq_bits(a)
#             a = _sq_bits(a)
#         return x
#     def factor_bits(x, n=2):
#         def _factor_bits(x):
#             a, ii, jj = {None}, None, None
#             for i in range(len(x)):
#                 for j in range(i+1, len(x)):
#                     b = x[i].intersection(x[j])
#                     if len(a) < len(b):
#                         a, ii, jj = b, i, j
#             return a, ii, jj
#         x = [i.copy() for i in x]
#         while True:
#             a, i, j = _factor_bits(x)
#             if len(a) < n:
#                 break
#             print((len(a), len(x)))
#             x[i] ^= a | {len(x)}
#             x[j] ^= a | {len(x)}
#             x.append(a)
#         return x
#     def visit(x, i):
#         y = set()
#         for j in x[i]:
#             if j < m:
#                 y.add(j)
#             else:
#                 y.update(visit(x, j))
#         return y
#     def visit(x, i):
#         y = set()
#         s = [i]
#         while s:
#             z = s.pop()
#             for j in z:
#                 if j < m:
#     i = 0
#     while i < len(x):
#         if len(x[i]) != 1:
#             i += 1
#         else:
#             a = next(iter(x[i]))
#             if a == i:
#                 i += 1
#             else:
#                 for j in range(len(x)):
#                     if a in x[j]:
#                         if x[j] & x[a]:
#                             raise Exception('error {} {} {}'.format(i, j, a))
#                         x[j] = (x[j] - {a}) | x[a]
#                 x[i] = x[a]
#                 a = x[i].pop()
#                 x[i] = x[a]
#                 b = x.pop(a)
#                 if a < i:
#                     i -= 1
#                 for j, b in enumerate(x):
#                     if j != i:
#                         x[j] = {c if c < a else c - 1 if c != a else i for c in b}
#         if len(x[i]) == 1:
#             a = x.pop(i).pop()
#             for j, k in enumerate(z):
#                 x[j] = {j if j < i else j - 1 if j != i else a for j in k}
#         return x


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
