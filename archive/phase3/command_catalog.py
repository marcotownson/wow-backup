import numpy as np
from scipy.linalg import dft
from collections import Counter

# --- Constants ---
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"
TIMESTEPS = 72
FREQUENCY_OFFSET_KEY = 1420.4556

# --- Known Commands (Rosetta Stone) ---
COMMAND_1 = "001110101001100100101101110000101111110011100001000110011100010011000111011110001001110000111110000011111110010011101101110100011101011101011001010110000010010101010011001000001011001011010101011100101111101000001010111010011110100100010100000110100110001011010111000110111011100001110111000110101000"
COMMAND_2 = "000010101100011101110000111011101100011101011010001100101100000101000100101111001011101010000010111110100111010101011010011010000010011001010101001000001101010011010111010111000101110110111001001111111000001111100001110010001111011100011001000111001100010000111001111110100001110110100100110010101110"
SPACER = "11111" # Note: This is a 5-bit chunk, not a 300-bit delta. It's for conceptual filtering.

KNOWN_COMMANDS = {
    COMMAND_1: "ACTIVATE",
    COMMAND_2: "DEACTIVATE"
}

def get_binary_state_at_timestep(initial_binary, t):
    """
    Runs the quantum evolution model for 't' steps and returns the binary state.
    """
    initial_state = np.array([int(bit) * 2 - 1 for bit in initial_binary], dtype=np.complex128)
    n = len(initial_state)
    qft_matrix = dft(n, scale='sqrtn')
    
    current_state = initial_state
    for i in range(t):
        evolved_state = np.dot(qft_matrix, current_state)
        phase_shift = np.exp(1j * 2 * np.pi * FREQUENCY_OFFSET_KEY * i / (TIMESTEPS * 1e6))
        current_state = evolved_state * phase_shift
        
    return "".join(['1' if np.real(c) >= 0 else '0' for c in current_state])

def analyze_timestep_deltas(initial_binary, total_timesteps):
    """
    Performs a bitwise XOR between consecutive timestep states to find the 'delta'.
    """
    all_states = [get_binary_state_at_timestep(initial_binary, t) for t in range(total_timesteps + 1)]
    return ["".join(['1' if a != b else '0' for a, b in zip(all_states[t+1], all_states[t])]) for t in range(total_timesteps)]

def catalog_commands(deltas):
    """
    Catalogs and analyzes the full list of XOR deltas.
    """
    # 1. Filter out known commands
    unknown_commands = [d for d in deltas if d not in KNOWN_COMMANDS]
    
    # 2. Catalog remaining commands and their frequencies
    print("--- Catalog of Unknown Commands ---")
    unknown_counts = Counter(unknown_commands)
    
    if not unknown_counts:
        print("No unknown commands found. All deltas match the Rosetta Stone.")
        return

    for command, count in unknown_counts.items():
        print(f"  - Command: {command[:30]}... (Found {count} time(s))")
        
    # 3. Cluster commands by prefix
    print("\n--- Command Clustering (by 3-bit prefix) ---")
    clusters = {}
    for command in unknown_counts:
        prefix = command[:3]
        if prefix not in clusters:
            clusters[prefix] = []
        clusters[prefix].append(command)
        
    for prefix, commands in clusters.items():
        print(f"\n  Cluster with prefix '{prefix}':")
        for cmd in commands:
            print(f"    - {cmd[:30]}...")

def main():
    """
    Runs the full command cataloging script.
    """
    print("=" * 50)
    print("  Full Command Language Catalog")
    print("=" * 50)
    
    # 1. Get all deltas
    deltas = analyze_timestep_deltas(BINARY_STRING, TIMESTEPS)
    
    # 2. Catalog and analyze
    catalog_commands(deltas)
    
    # 3. Interpretation
    print("\n" + "=" * 50)
    print("--- Interpretation ---")
    num_unique_unknown = len(set(d for d in deltas if d not in KNOWN_COMMANDS))
    print(f"Found {num_unique_unknown} unique unknown commands in addition to the known 'ACTIVATE' and 'DEACTIVATE' commands.")
    
    if num_unique_unknown < 10:
        print("The number of unique commands is very small, suggesting an elegant and simple language.")
        print("This implies a highly efficient instruction set where a few commands perform complex operations.")
    else:
        print("The number of unique commands is large, suggesting a complex language with many specific instructions.")
        print("This could mean the machine is capable of a wide variety of operations, each with its own command.")

if __name__ == "__main__":
    main()
