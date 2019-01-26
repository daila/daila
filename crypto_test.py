
def test_trace_bits():
    from crypto import m, reduction_poly, trace_bits
    def add(a, b):
        n = max(len(a), len(b))
        return [i + j for i, j in zip(
            a + [[]] * (n - len(a)), b + [[]] * (n - len(b))
        )]
    def shl(a, n):
        return [[]] * n + a
    def sq(a):
        x = []
        for i in range(m-1):
            x.extend([a[i], []])
        x.append(a[-1])
        for i in range(2):
            x, a = x[:m], x[m:]
            for n in reduction_poly:
                x = add(x, shl(a, n))
        return x
    def reduce(x):
        x = list(sorted(x))
        a = []
        i = 0
        while i < len(x) - 1:
            if x[i] == x[i+1]:
                i += 2
            else:
                a.append(x[i])
                i += 1
        if i == len(x) - 1:
            a.append(x[i])
        return a
    x = [[] for i in range(m)]
    a = [[i] for i in range(m)]
    for i in range(m):
        x = [reduce(i) for i in add(x, a)]
        a = [reduce(i) for i in sq(a)]
    bits = reduce(sum(x, []))
    assert bits == trace_bits


def test_trace():
    from crypto import m, reduction_poly, trace, fe_rand
    def sq(x):
        a = 0
        for i in range(m):
            if x & (2**i):
                a |= 2**(2*i)
        for i in range(2):
            x, a = a >> m, a % (2**m)
            for bit in reduction_poly:
                a ^= x << bit
        return a
    def tr(x):
        a = 0
        for i in range(m):
            a ^= x
            x = sq(x)
        x = 0
        for i in range(m):
            x ^= a % 2
            a >> 1
        return x
    assert all(tr(x) == trace(x) for x in (fe_rand() for i in range(100)))
