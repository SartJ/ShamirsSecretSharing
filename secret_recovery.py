# secret_recovery.py

from __future__ import print_function
import functools

# 12th Mersenne Prime
_PRIME = 2 ** 127 - 1

def _extended_gcd(a, b):
    x, last_x = 0, 1
    y, last_y = 1, 0
    while b != 0:
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x, last_y

def _divmod(num, den, p):
    inv, _ = _extended_gcd(den, p)
    return num * inv % p

def _lagrange_interpolate(x, x_s, y_s, p):
    k = len(x_s)
    def PI(vals):
        accum = 1
        for v in vals:
            accum *= v
        return accum
    nums = []
    dens = []
    for i in range(k):
        others = list(x_s)
        cur = others.pop(i)
        nums.append(PI(x - o for o in others))
        dens.append(PI(cur - o for o in others))
    den = PI(dens)
    num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p) for i in range(k)])
    return (_divmod(num, den, p) + p) % p

def recover_secret(shares, prime=_PRIME):
    if len(shares) < 3:
        raise ValueError("Need at least three shares.")
    x_s, y_s = zip(*shares)
    return _lagrange_interpolate(0, x_s, y_s, prime)

def main():
    import ast
    shares_input = input("Enter the shares as a list of tuples [(x1, y1), (x2, y2), ...]: ")
    shares = ast.literal_eval(shares_input)
    try:
        recovered_secret = recover_secret(shares)
        print("Is that what you are looking for:", recovered_secret)
    except ValueError as e:
        print(str(e))

if __name__ == '__main__':
    main()