# share_generation.py

# Compatibility imports for Python 2 and 3
from __future__ import print_function

# Standard library imports
import random
import functools

# Using the 12th Mersenne Prime as the modulus for operations to ensure a large finite field.
# This provides security by making it difficult to guess coefficients from shares due to the large size of the prime.
_PRIME = 2 ** 127 - 1

# Create a random integer function that is cryptographically secure by using SystemRandom,
# which provides randomness from the underlying operating system. It's suitable for cryptographic use.
_RINT = functools.partial(random.SystemRandom().randint, 0)

def _eval_at(poly, x, prime):
    """
    Evaluates a polynomial at a given value of x modulo a prime number.
   
    Args:
        poly (list): Coefficients of the polynomial, with the lowest power first.
        x (int): The point at which to evaluate the polynomial.
        prime (int): A prime number used as the modulus to ensure operations are in a finite field.
   
    Returns:
        int: The polynomial value at x modulo prime.
   
    Explanation:
        This function implements Horner's method to evaluate the polynomial efficiently.
        It processes each coefficient in reverse, starting from the highest power,
        which reduces the polynomial one degree at a time.
    """
    accum = 0
    for coeff in reversed(poly):
        accum = (accum * x + coeff) % prime
    return accum

def make_random_shares(secret, minimum, shares, prime=_PRIME):
    """
    Generates a specified number of shares for a given secret, using Shamir's Secret Sharing scheme.
   
    Args:
        secret (int): The secret to be shared.
        minimum (int): The minimum number of shares required to reconstruct the secret.
        shares (int): The total number of shares to create.
        prime (int): A prime number to use for modulo operations.
   
    Returns:
        list of tuples: Generated shares as (x, y) pairs.
   
    Raises:
        ValueError: If the minimum number of shares is greater than the total shares requested.
       
    Explanation:
        A random polynomial of degree (minimum-1) is created with the secret as the constant term.
        Other coefficients are randomly chosen. Shares are points on this polynomial, evaluated at
        distinct integers starting from 1 up to 'shares'.
    """
    if minimum > shares:
        raise ValueError("Pool secret would be irrecoverable.")
    # Create the polynomial with the secret as the first coefficient
    # and random coefficients for higher degrees.
    poly = [secret] + [_RINT(prime - 1) for i in range(minimum - 1)]
    # Generate shares as points on the polynomial
    points = [(i, _eval_at(poly, i, prime)) for i in range(1, shares + 1)]
    return points

def main():
    """
    Main function to interact with the user and generate shares based on input.
    """
    secret = int(input("Enter the secret number: "))
    shares = int(input("Enter the total number of shares: "))
    minimum = int(input("Enter the minimum number of shares needed to recover the secret: "))

    # Generate and display the shares
    generated_shares = make_random_shares(secret, minimum, shares)
    print("Generated Shares:")
    for share in generated_shares:
        print(share)

# Standard boilerplate to run the main function if this script is executed.
if __name__ == '__main__':
    main()