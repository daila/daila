
m = 251
reduction_poly = [7, 4, 2, 0]
trace_bits = [0, 247, 249]

def test_trace_bits():
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
                add(x, shl(a, n))
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
