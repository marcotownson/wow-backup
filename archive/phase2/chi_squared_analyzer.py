import numpy as np
from scipy.stats import chisquare
from collections import Counter

# The 300-bit binary string from the Wow! signal analysis
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"

def analyze_randomness_with_chi_squared(binary_data):
    """
    Performs a Chi-squared test to determine if the binary data
    significantly deviates from a random distribution.
    """
    print("--- Chi-Squared Test for Randomness ---")
    print("Methodology: This test compares the observed frequencies of 0s and 1s in the binary string to the frequencies that would be expected in a truly random sequence. A significant deviation suggests the data is not random.")

    # 1. Count observed frequencies
    counts = Counter(binary_data)
    observed_zeros = counts.get('0', 0)
    observed_ones = counts.get('1', 0)
    
    print(f"\nObserved Frequencies:")
    print(f"  - Zeros ('0'): {observed_zeros}")
    print(f"  - Ones  ('1'): {observed_ones}")

    # 2. Determine expected frequencies for a random distribution
    total_bits = len(binary_data)
    expected_frequency = total_bits / 2.0
    
    print(f"\nExpected Frequencies (for a random distribution of {total_bits} bits):")
    print(f"  - Zeros ('0'): {expected_frequency}")
    print(f"  - Ones  ('1'): {expected_frequency}")

    # 3. Perform the Chi-squared test
    observed_frequencies = [observed_zeros, observed_ones]
    expected_frequencies = [expected_frequency, expected_frequency]
    
    chi2_statistic, p_value = chisquare(f_obs=observed_frequencies, f_exp=expected_frequencies)

    print("\n--- Test Results ---")
    print(f"Chi-Squared Statistic: {chi2_statistic:.4f}")
    print(f"P-value: {p_value:.4f}")

    # 4. Interpret the results
    print("\n--- Interpretation ---")
    alpha = 0.05  # Standard significance level
    if p_value < alpha:
        print(f"The p-value ({p_value:.4f}) is less than the significance level ({alpha}).")
        print("Conclusion: We REJECT the null hypothesis that the data is random.")
        print("This provides strong statistical evidence that the binary string is NOT randomly distributed and likely has an artificial origin.")
    else:
        print(f"The p-value ({p_value:.4f}) is greater than the significance level ({alpha}).")
        print("Conclusion: We FAIL to reject the null hypothesis that the data is random.")
        print("This means there is no statistical evidence to suggest the binary string deviates from a random distribution.")

if __name__ == "__main__":
    analyze_randomness_with_chi_squared(BINARY_STRING)
