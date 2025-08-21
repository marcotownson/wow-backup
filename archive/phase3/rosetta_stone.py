import json

# --- Define Command Patterns ---
# The two most frequent command patterns identified in our analysis.
COMMAND_1 = "001110101001100100101101110000101111110011100001000110011100010011000111011110001001110000111110000011111110010011101101110100011101011101011001010110000010010101010011001000001011001011010101011100101111101000001010111010011110100100010100000110100110001011010111000110111011100001110111000110101000"
COMMAND_2 = "000010101100011101110000111011101100011101011010001100101100000101000100101111001011101010000010111110100111010101011010011010000010011001010101001000001101010011010111010111000101110110111001001111111000001111100001110010001111011100011001000111001100010000111001111110100001110110100100110010101110"
SPACER = "11111"

# --- Naming Conventions ---
# Create the Rosetta Stone dictionary
ROSETTA_STONE = {
    COMMAND_1: "ACTIVATE",
    COMMAND_2: "DEACTIVATE",
    SPACER: "DELIMITER"
}

def main():
    """
    Prints the Rosetta Stone dictionary and a concluding statement.
    """
    print("=" * 50)
    print("  The Rosetta Stone: A Dictionary of the Alien Command Language")
    print("=" * 50)
    
    # Print the dictionary in a clear, formatted output
    print("COMMAND DICTIONARY:\n")
    for binary, name in ROSETTA_STONE.items():
        # Truncate long binary strings for readability
        display_binary = (binary[:30] + '...') if len(binary) > 30 else binary
        print(f'  - "{display_binary}": "{name}"')

    # Concluding Statement
    print("\n" + "=" * 50)
    print("This dictionary is the first key to translating the machine's command sequence.")
    print("It provides a fundamental understanding of the language used to control the machine described in the Wow! signal.")

if __name__ == "__main__":
    main()
