import re

# The 300-bit binary string from the Wow! signal analysis
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"

import math

# --- Character Set and Equations ---
# Hypothetical 5-bit character mapping for equations
FIVE_BIT_MAP = {
    'E': '00001', 'm': '00010', 'c': '00011', '=': '00100',
    '^': '00101', '2': '00110', 'a': '00111', '+': '01000',
    'b': '01001', 'p': '01010', 'h': '01011', 'i': '01100',
    '(': '01101', '1': '01110', 's': '01111', 'q': '10000',
    'r': '10001', 't': '10010', '5': '10011', ')': '10100',
    '/': '10101'
}

EQUATIONS = {
    "E=mc^2": "E=mc^2",
    "Pythagorean Theorem": "a^2+b^2=c^2",
    "Golden Ratio Equation": "phi=(1+sqrt(5))/2",
}

# --- Constants for Fractional Analysis ---
CONSTANTS = {
    "Golden Ratio Value": (1 + math.sqrt(5)) / 2
}

def string_to_5bit_binary(s):
    """Converts a string to a 5-bit binary string using the custom map."""
    try:
        return ''.join(FIVE_BIT_MAP[char] for char in s)
    except KeyError as e:
        print(f"Character {e} not found in 5-bit map.")
        return None

def search_with_5bit_encoding(binary_data):
    """
    Searches for equations using the 5-bit encoding.
    """
    print("--- Analysis 1: Searching with 5-Bit Encoding ---")
    found_match = False
    for name, equation in EQUATIONS.items():
        equation_binary = string_to_5bit_binary(equation)
        if not equation_binary:
            continue
        
        print(f"\nSearching for: {name} ('{equation}')")
        print(f"  - 5-Bit Binary Pattern: {equation_binary}")
        
        match = re.search(equation_binary, binary_data)
        if match:
            print(f"  -> FOUND at bit position: {match.start()}")
            found_match = True
        else:
            print("  -> Not found.")
    return found_match

def analyze_as_fraction(binary_data):
    """
    Interprets the binary string as a fixed-point fraction and compares to constants.
    """
    print("\n--- Analysis 2: Interpreting as a Fraction ---")
    # Interpret the 300-bit string as a fixed-point number between 0 and some integer max.
    # A common way is to treat it as integer / 2^length.
    # To get a number > 1, we can scale it. Let's try scaling to the first 8 bits as integer part.
    integer_part_str = binary_data[:8]
    fractional_part_str = binary_data[8:]
    
    integer_part = int(integer_part_str, 2)
    fractional_part = int(fractional_part_str, 2) / (2**len(fractional_part_str))
    
    value = integer_part + fractional_part
    print(f"Interpreted value (8-bit integer, 292-bit fraction): {value:.6f}")
    
    found_match = False
    for name, const_val in CONSTANTS.items():
        print(f"Comparing to {name}: {const_val:.6f}")
        # Check if the values are very close (e.g., within 0.1% tolerance)
        if abs(value - const_val) / const_val < 0.001:
            print(f"  -> MATCH FOUND! The interpreted value is very close to {name}.")
            found_match = True
        else:
            print("  -> No match.")
    return found_match

def main():
    """
    Runs the equation finder script with multiple analysis methods.
    """
    print("=" * 50)
    print("  Advanced Equation Finder Analysis")
    print("=" * 50)
    
    # Run both analyses
    match1 = search_with_5bit_encoding(BINARY_STRING)
    match2 = analyze_as_fraction(BINARY_STRING)
    
    print("\n--- Final Interpretation ---")
    if match1 or match2:
        print("A potential match was found, suggesting the signal may contain encoded mathematical or physical constants.")
        print("This strengthens the hypothesis of an intelligent, artificial origin.")
    else:
        print("No matches were found with the tested 5-bit encoding or fractional interpretation.")
        print("This could mean:")
        print("  - The encoding scheme is different from the one hypothesized.")
        print("  - The fractional interpretation is incorrect (e.g., different bit allocation for integer/fraction).")
        print("  - The message contains other types of information.")

if __name__ == "__main__":
    main()
