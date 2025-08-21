import crcmod

# --- Constants ---
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"
EXPECTED_CHECKSUM = 1868

def simple_summation_checksum(binary_data):
    """
    Calculates the checksum by summing the integer values of the bits.
    """
    print("--- Checksum Method 1: Simple Summation ---")
    
    # Convert binary string to a list of integers and sum Fthem
    checksum = sum([int(bit) for bit in binary_data])
    
    print(f"Calculated Sum: {checksum}")
    print(f"Expected Checksum: {EXPECTED_CHECKSUM}")
    
    if checksum == EXPECTED_CHECKSUM:
        print("Result: MATCH FOUND.")
        print("Interpretation: This provides strong evidence that 1868 could be a simple sum checksum, but this is a very basic method and could be a coincidence.")
    else:
        print("Result: No match.")
        print("Interpretation: 1868 is not a simple sum of the bits.")
    print("-" * 20)

def crc16_checksum(binary_data):
    """
    Calculates the CRC-16 checksum of the binary data.
    """
    print("\n--- Checksum Method 2: CRC-16 ---")
    
    # The binary string needs to be converted to bytes
    byte_data = int(binary_data, 2).to_bytes((len(binary_data) + 7) // 8, byteorder='big')
    
    # Standard CRC-16 function (CRC-16-CCITT)
    crc16_func = crcmod.predefined.mkPredefinedCrcFun('crc-16')
    checksum = crc16_func(byte_data)
    
    print(f"Calculated CRC-16 Checksum: {checksum}")
    print(f"Expected Checksum: {EXPECTED_CHECKSUM}")
    
    if checksum == EXPECTED_CHECKSUM:
        print("Result: MATCH FOUND.")
        print("Interpretation: A match with a standard CRC-16 algorithm is a very strong indicator that 1868 is a checksum for error detection.")
    else:
        print("Result: No match.")
        print("Interpretation: 1868 is not a standard CRC-16 checksum. A different polynomial or CRC variant might have been used.")
    print("-" * 20)

def xor_sum_checksum(binary_data):
    """
    Calculates the checksum by XORing chunks of the data.
    """
    print("\n--- Checksum Method 3: XOR Sum ---")
    
    # Pad the data to be divisible by 16 bits
    padded_data = binary_data + '0' * (16 - len(binary_data) % 16)
    
    # Split into 16-bit chunks
    chunks = [padded_data[i:i+16] for i in range(0, len(padded_data), 16)]
    
    # XOR all chunks together
    xor_sum = 0
    for chunk in chunks:
        xor_sum ^= int(chunk, 2)
        
    print(f"Calculated XOR Sum (16-bit chunks): {xor_sum}")
    print(f"Expected Checksum: {EXPECTED_CHECKSUM}")
    
    if xor_sum == EXPECTED_CHECKSUM:
        print("Result: MATCH FOUND.")
        print("Interpretation: This is a strong indicator that 1868 is an XOR checksum, a common method for simple error checking.")
    else:
        print("Result: No match.")
        print("Interpretation: 1868 is not a 16-bit XOR checksum. The chunk size or method could be different.")
    print("-" * 20)

def main():
    """
    Runs all checksum analysis functions.
    """
    print("=" * 50)
    print("  Checksum Analysis with Key 1868")
    print("=" * 50)
    
    simple_summation_checksum(BINARY_STRING)
    crc16_checksum(BINARY_STRING)
    xor_sum_checksum(BINARY_STRING)

if __name__ == "__main__":
    # First, ensure the required libraries are installed.
    try:
        import crcmod
    except ImportError:
        print("crcmod is not installed. Please install it using: pip install crcmod")
    else:
        main()
