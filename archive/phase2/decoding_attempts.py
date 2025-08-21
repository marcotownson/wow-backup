import numpy as np
import random
import matplotlib.pyplot as plt
import base64

# --- Constants ---
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"
DECODING_KEY = 1868

def xor_with_key(binary_data, key):
    """
    Performs a bitwise XOR operation with a repeating key.
    """
    print("--- Decoding Method 1: XOR with Key ---")
    
    # Convert key to a binary string
    key_binary = bin(key)[2:]
    
    # Repeat the key to match the length of the binary data
    repeated_key = (key_binary * (len(binary_data) // len(key_binary) + 1))[:len(binary_data)]
    
    # Perform XOR operation
    xored_result = "".join(['1' if a != b else '0' for a, b in zip(binary_data, repeated_key)])
    
    print(f"Key (1868) in binary: {key_binary}")
    print(f"XOR result: {xored_result}")
    print("-" * 20)
    return xored_result

def ascii_decoding_with_offset(binary_data, key):
    """
    Attempts to decode the binary string as ASCII text, with and without an offset.
    """
    print("\n--- Decoding Method 2: ASCII Decoding with Offset ---")
    
    # Split into 8-bit chunks (bytes)
    # The 300-bit string is not perfectly divisible by 8, so we'll pad it.
    padded_data = binary_data + '0' * (8 - len(binary_data) % 8)
    byte_chunks = [padded_data[i:i+8] for i in range(0, len(padded_data), 8)]
    
    # --- Attempt 1: Direct ASCII decoding ---
    try:
        decoded_bytes = [int(chunk, 2) for chunk in byte_chunks]
        ascii_text = "".join([chr(b) for b in decoded_bytes if 32 <= b <= 126])
        print(f"Direct ASCII decoding result (printable chars only): {ascii_text or 'No printable characters found.'}")
    except Exception as e:
        print(f"Direct ASCII decoding failed: {e}")

    # --- Attempt 2: Decoding with offset ---
    offset = key % 256
    print(f"\nApplying offset: {offset}")
    try:
        offset_bytes = [(int(chunk, 2) + offset) % 256 for chunk in byte_chunks]
        offset_ascii_text = "".join([chr(b) for b in offset_bytes if 32 <= b <= 126])
        print(f"Offset ASCII decoding result (printable chars only): {offset_ascii_text or 'No printable characters found.'}")
    except Exception as e:
        print(f"Offset ASCII decoding failed: {e}")
        
    print("-" * 20)

def image_manipulation_with_key(binary_data, key):
    """
    Uses the key as a seed to shuffle the bits and create a new image.
    """
    print("\n--- Decoding Method 3: Image Manipulation with Key ---")
    
    # Use the key as a seed for the random number generator
    random.seed(key)
    
    # Create a permutation map
    indices = list(range(len(binary_data)))
    random.shuffle(indices)
    
    # Shuffle the binary string
    shuffled_list = ['0'] * len(binary_data)
    for i, original_pos in enumerate(indices):
        shuffled_list[i] = binary_data[original_pos]
    shuffled_binary = "".join(shuffled_list)
    
    # Create an image from the shuffled data (20x15)
    width, height = 20, 15
    pixels = np.array([int(bit) for bit in shuffled_binary]).reshape((height, width))
    
    plt.figure(figsize=(8, 6))
    plt.imshow(pixels, cmap='gray_r', interpolation='nearest')
    plt.title(f"Image from Shuffled Binary (Seed: {key})")
    
    output_path = "shuffled_image.png"
    plt.savefig(output_path)
    print(f"Shuffled image saved to '{output_path}'")
    plt.close()
    
    print("Interpretation: The original and shuffled images can be visually compared.")
    print("If the shuffled image reveals a clear pattern, it could mean the key (1868) is a seed used to encode the message.")
    print("-" * 20)

def main():
    """
    Runs all decoding attempts.
    """
    print("=" * 50)
    print("  Decoding Attempts Using Key 1868")
    print("=" * 50)
    
    xor_with_key(BINARY_STRING, DECODING_KEY)
    ascii_decoding_with_offset(BINARY_STRING, DECODING_KEY)
    image_manipulation_with_key(BINARY_STRING, DECODING_KEY)

if __name__ == "__main__":
    main()
