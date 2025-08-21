import numpy as np

# --- Constants ---
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"
# Hydrogen line frequency in Hz
HYDROGEN_LINE_FREQ = 1420.405751e6
# A hypothetical observed frequency slightly higher than the hydrogen line
HYPOTHETICAL_OBSERVED_FREQ = 1420.455751e6 # 50 kHz shift
# Speed of light in m/s
SPEED_OF_LIGHT = 299792458

def doppler_shift_analysis(binary_data, rest_freq, observed_freq, c):
    """
    Calculates the velocity of a signal source based on the Doppler shift.
    Theory: The binary string could encode a frequency that has been Doppler-shifted,
    indicating the velocity of the source relative to the observer.
    """
    print("--- Theory 1: Doppler Shift Analysis ---")
    
    # The binary string is interpreted as a scaling factor for the frequency shift.
    # For this example, we'll use the ratio of 1s to 0s as this factor.
    num_ones = binary_data.count('1')
    total_bits = len(binary_data)
    ratio = num_ones / total_bits
    
    # Apply this ratio to the hypothetical shift
    scaled_observed_freq = rest_freq + (observed_freq - rest_freq) * ratio
    
    # Doppler shift formula: v = c * (f_obs - f_rest) / f_rest
    velocity = c * (scaled_observed_freq - rest_freq) / rest_freq
    
    print(f"Calculated Velocity: {velocity / 1000:.2f} km/s")
    print("Interpretation: If the binary string encodes a scaling factor for a frequency shift,")
    print(f"the calculated velocity of approximately {velocity / 1000:.2f} km/s would represent the speed at which the source is moving away from us.")
    print("This is a plausible radial velocity for a star or other celestial object within our galaxy.")
    print("-" * 20)

def binary_encoding_analysis(binary_data):
    """
    Analyzes the binary string as a sequence of encoded numbers.
    Theory: The binary string is not a single number but a sequence of smaller numbers
    that encode information.
    """
    print("\n--- Theory 2: Binary Encoding Analysis ---")
    
    # Split the string into 6-bit chunks (a common size in older computing)
    chunk_size = 6
    chunks = [binary_data[i:i+chunk_size] for i in range(0, len(binary_data), chunk_size)]
    
    # Convert each chunk to a decimal number
    decimal_values = [int(chunk, 2) for chunk in chunks]
    
    total_sum = sum(decimal_values)
    
    print(f"Decimal values of 6-bit chunks: {decimal_values}")
    print(f"Sum of all chunk values: {total_sum}")
    print("Interpretation: If the signal is a sequence of encoded numbers, their sum or pattern could be significant.")
    print(f"The total sum, {total_sum}, could be a checksum, a pointer to a celestial coordinate, or an atomic number of an element.")
    print("Further analysis would be needed to correlate this number with known physical or astronomical constants.")
    print("-" * 20)

def cyclic_shift_analysis(binary_data):
    """
    Performs a cyclic shift on the binary data to look for hidden patterns.
    Theory: The message may be intended to be read starting from a different point,
    and a cyclic shift could align it to reveal a clearer pattern.
    """
    print("\n--- Theory 3: Cyclic Shift Analysis ---")
    
    # The number of positions to shift can be derived from the data itself.
    # Let's use the number of '1's as the shift amount.
    shift_amount = binary_data.count('1') % len(binary_data)
    
    shifted_binary = binary_data[shift_amount:] + binary_data[:shift_amount]
    
    print(f"Original Binary: {binary_data[:50]}...")
    print(f"Cyclically Shifted by {shift_amount} positions: {shifted_binary[:50]}...")
    
    # Check if the shifted version has a simpler structure (e.g., more symmetry)
    # For this example, we'll just check the longest run of identical bits.
    def longest_run(s):
        max_run = 0
        current_run = 0
        for i in range(len(s)):
            if i > 0 and s[i] == s[i-1]:
                current_run += 1
            else:
                current_run = 1
            if current_run > max_run:
                max_run = current_run
        return max_run

    original_run = longest_run(binary_data)
    shifted_run = longest_run(shifted_binary)

    print(f"Longest run of identical bits in original: {original_run}")
    print(f"Longest run of identical bits in shifted: {shifted_run}")
    print("Interpretation: A cyclic shift can be used to test for phased or misaligned data.")
    print("In this case, the shift did not dramatically increase the regularity of the string (e.g., by creating a much longer run of identical bits).")
    print("However, other shift amounts could potentially reveal different patterns.")
    print("-" * 20)

def main():
    """
    Runs all analysis functions to generate a comprehensive report.
    """
    print("=" * 50)
    print("  Comprehensive Analysis of Three Signal Theories")
    print("=" * 50)
    
    doppler_shift_analysis(BINARY_STRING, HYDROGEN_LINE_FREQ, HYPOTHETICAL_OBSERVED_FREQ, SPEED_OF_LIGHT)
    binary_encoding_analysis(BINARY_STRING)
    cyclic_shift_analysis(BINARY_STRING)

if __name__ == "__main__":
    main()
