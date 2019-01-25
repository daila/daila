
sc_modulus = 2**249 + 17672450755679567125975931502191870417
fe_modulus = 2**251 + 2**7 + 2**4 + 2**2 + 1
d1 = 2**57 + d**54 + d**44 + 1

m = 251
reduction_poly = [7, 4, 2, 0]
trace_bits = [0, 247, 249]


def fe_mul(a, b):
    c = 0
    while b:
        if b & 1:
            c ^= a
        a <<= 1
        b >>= 1
    if c < 2**251:
        return c
    return (c % 2**251) ^ fe_mul(c >> 251, 2**7 + 2**4 + 2**2 + 1)


def fe_sq(a):
    return fe_mul(a, a)


d1d1 = fe_mul(d1, d1)


def fe_exp(x, n):
    xx = 1
    while n:
        if n & 1:
            xx = fe_mul(xx, x)
        x = fe_mul(x, x)
        n >>= 1
    return xx


def fe_sqrt(x):
    # pth root of x = x ^ (p ^ (m - 1)), for x in G(2^m)
    return fe_exp(x, 2**250)


sqrtd1 = fe_sqrt(d1)


def fe_inv(x):
    return fe_exp(x, 2**251 - 2)


def fe_rand():
    return fe_mul(sum(x << (8*i) for i, x in enumerate(urandom(32))), 1)


def trace(x):
    s = 0
    for bit in trace_bits:
        s ^= (x >> bit) & 1
    return s


def htrace(x):
    pass


def ge_add(P, Q):
    # https://hyperelliptic.org/EFD/g12o/auto-edwards-xyz-1.html
    # add-2008-blr-3
    (X1, Y1, Z1) = P
    (X2, Y2, Z2) = Q
    A = fe_mul(X1, X2)
    B = fe_mul(Y1, Y2)
    C = fe_mul(Z1, Z2)
    D = fe_mul(d1, C)
    E = fe_mul(C, C)
    F = fe_mul(d1d1, E)
    G = fe_mul(X1 ^ Z1, X2 ^ Z2)
    H = fe_mul(Y1 ^ Z1, Y2 ^ Z2)
    I = A ^ G
    J = B ^ H
    K = fe_mul(X1 ^ Y1, X2 ^ Y2)
    L = fe_mul(d1, K)
    U = fe_mul(C, F ^ fe_mul(L, K ^ I ^ J ^ C))
    V = U ^ fe_mul(D, F) ^ fe_mul(
        L, fe_mul(d1, E) ^ fe_mul(G, H) ^ fe_mul(A, B)
    )
    X3 = V ^ fe_mul(fe_mul(D, A ^ D), G ^ D)
    Y3 = V ^ fe_mul(fe_mul(D, B ^ D), H ^ D)
    Z3 = U
    return (X3, Y3, Z3)


def ge_dbl(P):
    # https://hyperelliptic.org/EFD/g12o/auto-edwards-xyz-1.html
    # dbl-2008-blr-2
    (X1, Y1, Z1) = P
    W1 = X1 ^ Y1
    E = fe_sq(fe_mul(W1, W1 ^ Z1))
    X3 = fe_sq(
        fe_mul(fe_mul(sqrtd1, W1) ^ X1, Z1) ^ fe_sq(X1)
    )
    Y3 = X3 ^ E
    Z3 = E ^ fe_mul(d1, fe_sq(fe_sq(Z1)))
    return (X3, Y3, Z3)

    

