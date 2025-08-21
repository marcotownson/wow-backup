# --- Constants ---
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"

# --- Atomic Binary Patterns ---
ATOMIC_NUMBERS = {
    "Hydrogen": 1, "Helium": 2, "Lithium": 3, "Beryllium": 4, "Boron": 5,
    "Carbon": 6, "Nitrogen": 7, "Oxygen": 8, "Fluorine": 9, "Neon": 10,
    "Sodium": 11, "Magnesium": 12, "Aluminum": 13, "Silicon": 14, "Phosphorus": 15,
    "Sulfur": 16, "Chlorine": 17, "Argon": 18, "Potassium": 19, "Calcium": 20
}

ATOMIC_BINARY = {name: bin(num)[2:] for name, num in ATOMIC_NUMBERS.items()}

def search_for_formulas(binary_data):
    """
    Searches for specific chemical formula patterns in the binary string.
    """
    print("--- Searching for Chemical Formula Patterns ---")

    # 1. Define the formula patterns to search for
    patterns = {
        "H2He (H-H-He)": ATOMIC_BINARY["Hydrogen"] * 2 + ATOMIC_BINARY["Helium"],
        "CH4 (C-H-H-H-H)": ATOMIC_BINARY["Carbon"] + ATOMIC_BINARY["Hydrogen"] * 4,
        "H2O (H-H-O)": ATOMIC_BINARY["Hydrogen"] * 2 + ATOMIC_BINARY["Oxygen"]
    }

    # 2. Search for each pattern
    found_match = False
    for name, pattern in patterns.items():
        index = binary_data.find(pattern)
        print(f"\nSearching for: {name}")
        print(f"  - Combined Binary Pattern: {pattern}")
        if index != -1:
            print(f"  -> FOUND at bit position: {index}")
            found_match = True
        else:
            print("  -> Not found.")

    # 3. Interpretation
    print("\n--- Interpretation ---")
    if found_match:
        print("A match for a multi-element chemical formula has been found.")
        print("This is a significant result, as it suggests a higher level of complexity than just a list of elements.")
        print("Finding a specific compound could indicate a 'blueprint' or a message about specific chemical processes, like fusion.")
    else:
        print("No matches were found for the tested chemical formulas (H2He, CH4).")
        print("This could mean:")
        print("  - The theory is incorrect.")
        print("  - The elements are encoded in a different order or format.")
        print("  - The signal is describing different chemical compounds.")

def main():
    """
    Runs the chemical formula analysis script.
    """
    print("=" * 50)
    print("  Chemical Formula Blueprint Analysis")
    print("=" * 50)
    search_for_formulas(BINARY_STRING)

if __name__ == "__main__":
    main()
