
from crypto_test import (
    test_fe_sq, test_fe_sqrt, test_fe_inv,
    test_trace_bits, test_trace, test_half_trace
)

print("Running test_fe_sq...", end="")
print(("FAIL", "PASS")[test_fe_sq()])

print("Running test_fe_sqrt...", end="")
print(("FAIL", "PASS")[test_fe_sqrt()])

print("Running test_fe_inv...", end="")
print(("FAIL", "PASS")[test_fe_inv()])

print("Running test_trace_bits...", end="")
print(("FAIL", "PASS")[test_trace_bits()])

print("Running test_trace...", end="")
print(("FAIL", "PASS")[test_trace()])

print("Running test_half_trace...", end="")
print(("FAIL", "PASS")[test_half_trace()])
