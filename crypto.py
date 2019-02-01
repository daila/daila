
from os import urandom

m = 251
d1 = 2**57 + 2**54 + 2**44 + 1
reduction_poly_bits = [7, 4, 2, 0]
trace_bits = [0, 247, 249]

ge_0 = (0, 0, 1)

ge_1 = (
    3365420101509117344964743535870703383766329479200211359486628581714619492652,
    2437893306741284650320547128292229629793566075353469778729552340321738740790,
    1
)

sc_0 = 2**249 + 17672450755679567125975931502191870417


def fe_mul(a, b):
    c = 0
    for i in range(m):
        c ^= a & (-(b & 1))
        a <<= 1
        b >>= 1
    for i in range(2):
        a, c = c >> m, c % (2**m)
        for bit in reduction_poly_bits:
            c ^= a << bit
    return c


def fe_sq(x):
    a = 0
    for i in range(m):
        a |= (x & (1 << i)) << i
    for i in range(2):
        x, a = a >> m, a % (2**m)
        for bit in reduction_poly_bits:
            a ^= x << bit
    return a


d1d1 = fe_sq(d1)


def fe_multisq(x, n):
    for i in range(n):
        x = fe_sq(x)
    return x

def fe_exp(x, n):
    xx = 1
    while n:
        if n & 1:
            xx = fe_mul(xx, x)
        x = fe_mul(x, x)
        n >>= 1
    return xx


def fe_sqrt(x):
    # pth root of x = x ** (p ** (m - 1)), for x in G(p ** m)
    return fe_exp(x, 2**250)


sqrtd1 = fe_sqrt(d1)


def fe_inv(x):
    # return x ** -1 == x ** (2 ** 251 - 2 ** 1)
    a_1_0   = x
    a_2_0   = fe_mul (fe_multisq (a_1_0,   1),   a_1_0)
    a_4_0   = fe_mul (fe_multisq (a_2_0,   2),   a_2_0)
    a_5_0   = fe_mul (fe_multisq (a_4_0,   1),   a_1_0)
    a_10_0  = fe_mul (fe_multisq (a_5_0,   5),   a_5_0)
    a_15_0  = fe_mul (fe_multisq (a_10_0,  5),   a_5_0)
    a_30_0  = fe_mul (fe_multisq (a_15_0,  15),  a_15_0)
    a_60_0  = fe_mul (fe_multisq (a_30_0,  30),  a_30_0)
    a_120_0 = fe_mul (fe_multisq (a_60_0,  60),  a_60_0)
    a_125_0 = fe_mul (fe_multisq (a_120_0, 5),   a_5_0)
    a_250_0 = fe_mul (fe_multisq (a_125_0, 125), a_125_0)
    a_251_1 = fe_sq (a_250_0)
    return a_251_1


def fe_rand():
    return fe_frombytes(urandom(32))


def trace(x):
    s = 0
    for bit in trace_bits:
        s ^= (x >> bit) & 1
    return s


def half_trace(x):
    def htr(x):
        a = 0
        for i in range((m-1)//2 + 1):
            a ^= x
            x = fe_sq(x)
            x = fe_sq(x)
        return a
    return htr(x)


def fe_frombytes(s):
    return sum(x << (8*i) for i, x in enumerate(s)) % (2 ** m)


def fe_tobytes(x):
    return bytearray((x >> (8 * i)) & 0xff for i in range(32))


def isoncurve(P):
    # (d + x + x^2) (y^2 + y) = d (x + x^2)
    if P[-1] != 1:
        P = ge_norm(P)
    x, y, z = P
    xx, yy = fe_sq(x) ^ x, fe_sq(y) ^ y
    return fe_mul(d1 ^ xx, yy) == fe_mul(d1, xx)


def ge_rand():
    return ge_frombytes(urandom(32))


def ge_frombytes(s):
    # d (x + x^2 + y + y^2) = x y + x y (x + y) + x^2 y^2
    # d x + d x^2 + d y + d y^2 = x y + x^2 y + x y^2 + x^2 y^2
    # (d + x + x^2) (y^2 + y) = d (x + x^2)
    # y^2 + y = d (x + x^2) / (d + x + x^2) = b
    x = fe_frombytes(s)
    xx = fe_sq(x) ^ x
    b = fe_mul(fe_mul(d1, xx), fe_inv(d1 ^ xx))
    return (x, (half_trace(b) & -2) | (x & 1), 1) if trace(b) == 0 else None


def ge_tobytes(P):
    s = None
    return s


def ge_norm(P):
    x, y, z = P
    z = fe_inv(z)
    return fe_mul(x, z), fe_mul(y, z), 1


def ge_mul(P, n):
    Q = ge_0
    while n:
        if n & 1:
            Q = ge_add(Q, P)
        P = ge_dbl(P)
        n >>= 1
    return Q


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
