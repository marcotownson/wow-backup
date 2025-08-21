import numpy as np
import matplotlib.pyplot as plt
from sympy import isprime
import os

# --- Configuration ---
ENCRYPTED_SIGNAL = "HEQUJ5"
SIGNAL_BASE = 72
DECRYPTION_KEY = 11
OUTPUT_DIR = "wow_signal_xor_decryption"

# --- Helper Functions ---

def sequence_to_decimal(sequence, base):
    """Converts a full alphanumeric sequence to a base-10 decimal integer."""
    decimal_value = 0
    power = len(sequence) - 1
    for digit in sequence:
        if '0' <= digit <= '9':
            digit_val = int(digit)
        else:
            digit_val = 10 + (ord(digit) - ord('A'))
        if digit_val >= base:
            return None
        decimal_value += digit_val * (base ** power)
        power -= 1
    return decimal_value

def repeating_key_xor(binary_message, key_int):
    """Performs a repeating key XOR operation."""
    key_binary = bin(key_int)[2:]
    decrypted_bits = []
    for i, bit in enumerate(binary_message):
        key_bit = key_binary[i % len(key_binary)]
        decrypted_bit = str(int(bit) ^ int(key_bit))
        decrypted_bits.append(decrypted_bit)
    return "".join(decrypted_bits)

def analyze_payload(binary_str):
    """Performs a full analysis on a decrypted binary string."""
    print("\n--- 2. Analyzing Decrypted Payload ---")
    length = len(binary_str)
    print(f" -> Payload length: {length} bits")

    # Shannon Entropy
    ones = binary_str.count('1')
    prob_one = ones / length
    entropy = - (prob_one * np.log2(prob_one) + (1-prob_one) * np.log2(1-prob_one))
    print(f" -> Shannon Entropy: {entropy:.4f}")

    # Primality Check
    payload_decimal = int(binary_str, 2)
    print(f" -> Decimal Value: {payload_decimal}")
    if isprime(payload_decimal):
        print("\n*** MAJOR FINDING: The decrypted payload is a PRIME NUMBER. ***")
    else:
        print(" -> Payload is not a prime number.")

    # Visual Analysis (if possible)
    if length == 300: # We use 300 as it's our previously confirmed message size
        print(" -> Visualizing payload as a 20x15 image...")
        pixels = np.array([int(bit) for bit in binary_str]).reshape((15, 20))
        plt.figure(figsize=(10, 7.5))
        plt.imshow(pixels, cmap='gray_r', interpolation='nearest')
        plt.title("Decrypted Payload as a 20x15 Image")
        filepath = os.path.join(OUTPUT_DIR, "decrypted_image.png")
        plt.savefig(filepath)
        plt.close()
        print(f" -> Saved visualization to: {filepath}")

# --- Main Execution ---
if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("="*60); print("--- Decrypting with XOR Key 11 Hypothesis ---"); print("="*60)

    # 1. Convert the encrypted signal to its full binary representation
    print("\n--- 1. Converting Encrypted Signal ---")
    signal_decimal = sequence_to_decimal(ENCRYPTED_SIGNAL, SIGNAL_BASE)
    signal_binary = bin(signal_decimal)[2:]
    print(f" -> '{ENCRYPTED_SIGNAL}' (Base {SIGNAL_BASE}) = {signal_decimal} (Base 10)")
    print(f" -> Encrypted binary length: {len(signal_binary)} bits")

    # 2. Decrypt using the repeating XOR key
    decrypted_binary = repeating_key_xor(signal_binary, DECRYPTION_KEY)
    
    # 3. Analyze the decrypted payload
    analyze_payload(decrypted_binary)

    print("\n" + "="*60); print("--- DECRYPTION & ANALYSIS COMPLETE ---"); print("="*60)