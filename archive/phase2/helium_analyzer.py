# --- Constants ---
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"
HELIUM_ATOMIC_NUMBER = 2
# To convert the atomic mass to an integer for binary representation, we multiply it by 1,000,000
HELIUM_ATOMIC_MASS = 4.002602
HELIUM_ATOMIC_MASS_INT = int(HELIUM_ATOMIC_MASS * 1_000_000)

# All prime atomic numbers up to the highest known element (118)
PRIME_ATOMIC_NUMBERS = {
    3: "Lithium", 5: "Boron", 7: "Nitrogen", 11: "Sodium", 13: "Aluminum",
    17: "Chlorine", 19: "Potassium", 23: "Vanadium", 29: "Copper", 31: "Gallium",
    37: "Rubidium", 41: "Niobium", 43: "Technetium", 47: "Silver", 53: "Iodine",
    59: "Praseodymium", 61: "Promethium", 67: "Holmium", 71: "Lutetium",
    73: "Tantalum", 79: "Gold", 83: "Bismuth", 89: "Actinium", 97: "Berkelium",
    101: "Mendelevium", 103: "Lawrencium", 107: "Bohrium", 109: "Meitnerium",
    113: "Nihonium"
}

def search_for_atomic_data(binary_data):
    """
    Scans the binary string for patterns related to atomic data.
    """
    print("--- Searching for Atomic Data Patterns ---")
    
    # 1. Define the patterns to search for
    patterns = {
        f"Helium Atomic Number ({HELIUM_ATOMIC_NUMBER})": bin(HELIUM_ATOMIC_NUMBER)[2:],
        f"Helium Atomic Mass ({HELIUM_ATOMIC_MASS_INT})": bin(HELIUM_ATOMIC_MASS_INT)[2:]
    }
    
    # Add other prime atomic numbers to the search
    for num, name in PRIME_ATOMIC_NUMBERS.items():
        patterns[f"{name} Atomic Number ({num})"] = bin(num)[2:]

    # 2. Scan the binary string for each pattern
    found_match = False
    for name, pattern in patterns.items():
        index = binary_data.find(pattern)
        print(f"\nSearching for: {name}")
        print(f"  - Binary Pattern: {pattern}")
        if index != -1:
            print(f"  -> FOUND at bit position: {index}")
            found_match = True
        else:
            print("  -> Not found.")
            
    # 3. Interpretation
    print("\n--- Interpretation ---")
    if found_match:
        print("The discovery of binary sequences corresponding to fundamental atomic numbers (especially Helium) is a significant finding.")
        print("This could imply that the signal is a deliberate message containing basic scientific information, akin to a 'universal' language based on physics.")
        print("Such a finding would strongly suggest an intelligent, artificial origin.")
    else:
        print("No direct matches for the tested atomic data were found.")
        print("This could mean several things:")
        print("  - The hypothesis is incorrect.")
        print("  - The data is encoded differently (e.g., with padding, different bit ordering, or a more complex format).")
        print("  - The signal contains different scientific information.")

def main():
    """
    Runs the analysis script.
    """
    print("=" * 50)
    print("  Helium Reference Analysis")
    print("=" * 50)
    search_for_atomic_data(BINARY_STRING)

if __name__ == "__main__":
    main()
