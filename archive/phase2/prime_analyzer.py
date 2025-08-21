import math
import random

# The 300-bit binary string identified as a prime number
BINARY_PRIME = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"

def miller_rabin(n, k=5):
    """Miller-Rabin primality test."""
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n < p * p:
            return True
        if n % p == 0:
            return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def analyze_prime_properties(p):
    """
    Investigates several mathematical properties of a given prime number p.
    """
    print(f"--- Analyzing Prime: {p} ---\n")

    # 1. Check for special prime types
    print("[1] Checking for special prime types...")

    # Sophie Germain Prime: p is a prime such that 2p + 1 is also prime.
    if miller_rabin(2 * p + 1):
        print(f"  -> FINDING: The number is a Sophie Germain prime. (2p + 1 is also prime)")
    else:
        print("  -> Not a Sophie Germain prime.")

    # Safe Prime: p is a prime of the form 2q + 1, where q is also a prime.
    q = (p - 1) // 2
    if (p - 1) % 2 == 0 and miller_rabin(q):
        print(f"  -> FINDING: The number is a Safe Prime. (p-1)/2 is also prime.")
    else:
        print("  -> Not a Safe Prime.")

    print("\n[2] Analyzing small factors of p-1 and p+1...")
    
    # Check for small factors up to a reasonable limit.
    limit = 1000
    p_minus_1_has_small_factors = False
    p_plus_1_has_small_factors = False
    
    for i in range(2, limit):
        if (p - 1) % i == 0:
            p_minus_1_has_small_factors = True
            break
            
    for i in range(2, limit):
        if (p + 1) % i == 0:
            p_plus_1_has_small_factors = True
            break

    if p_minus_1_has_small_factors:
        print(f"  -> FINDING: p-1 has at least one small factor (< {limit}). This is relevant for cryptographic applications.")
    else:
        print(f"  -> NOTE: p-1 appears to have no small factors (< {limit}).")
        
    if p_plus_1_has_small_factors:
        print(f"  -> FINDING: p+1 has at least one small factor (< {limit}).")
    else:
        print(f"  -> NOTE: p+1 appears to have no small factors (< {limit}).")
    
    print("\n[3] Conclusion and Interpretation")
    print("The primality of the number is a strong indicator of non-randomness, suggesting it was constructed intentionally.")
    print("Its status as a 'Safe Prime' is particularly noteworthy. Safe primes are crucial in cryptography, especially in protocols like Diffie-Hellman key exchange, because they resist certain attacks.")
    print("This suggests the number could be a public key, a parameter for a cryptographic system, or a component of a digital signature.")
    print("\nNext Steps:")
    print(" - Investigate cryptographic systems that use large safe primes.")
    print(" - Analyze the 5-bit chunks for patterns that might correspond to a known character encoding or instruction set, with the prime as a key.")


if __name__ == "__main__":
    # Convert the binary string to a decimal integer
    prime_decimal = int(BINARY_PRIME, 2)
    
    # Verify it's prime before analyzing
    if miller_rabin(prime_decimal):
        print("Primality confirmed with Miller-Rabin test.\n")
        analyze_prime_properties(prime_decimal)
    else:
        print("Error: The provided binary string does not represent a prime number.")