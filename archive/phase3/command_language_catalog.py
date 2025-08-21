import numpy as np
from scipy.linalg import dft
from collections import Counter

# --- Constants ---
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"
TIMESTEPS = 72
FREQUENCY_OFFSET_KEY = 1420.4556

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

def generate_command_catalog(deltas):
    """
    Generates a clean, readable, and comprehensive catalog of the command language.
    """
    # 1. Get unique deltas and their counts
    delta_counts = Counter(deltas)
    unique_deltas = sorted(delta_counts.keys())
    
    # 2. Group by prefix
    clusters = {}
    for delta in unique_deltas:
        prefix = delta[:3]
        if prefix not in clusters:
            clusters[prefix] = []
        clusters[prefix].append(delta)
        
    # 3. Print the catalog
    print("=" * 70)
    print("  Comprehensive Catalog of the Command Language")
    print("=" * 70)
    
    for prefix, commands in sorted(clusters.items()):
        print(f"\n--- Command Cluster (Prefix: {prefix}) ---")
        for command in sorted(commands):
            count = delta_counts[command]
            print(f"  - {command[:40]}... (Found {count} time(s))")
            
    # 4. Interpretation
    print("\n" + "=" * 70)
    print("--- Interpretation of the Command Catalog ---")
    print("The command language appears to be structured into distinct families, as indicated by the common prefixes.")
    print("This suggests a hierarchical or organized instruction set. For example:")
    print("  - Commands with prefix '000' might relate to logical or computational operations, such as state resets or data manipulation.")
    print("  - Commands with prefix '001' could be related to physical or structural changes, like activating or deactivating components.")
    print("\nThis catalog provides a clear and organized view of the entire command set, which is the next step in fully deciphering the machine's operational language.")

def main():
    """
    Runs the full command cataloging script.
    """
    # 1. Get all deltas
    deltas = analyze_timestep_deltas(BINARY_STRING, TIMESTEPS)
    
    # 2. Generate the catalog
    generate_command_catalog(deltas)

if __name__ == "__main__":
    main()
