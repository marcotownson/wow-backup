import numpy as np
from scipy.linalg import dft
from collections import Counter

# --- Constants ---
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"
TIMESTEPS = 72
# Constants from the original model for consistency
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
        # The phase shift is part of the original model, so we include it for accuracy
        phase_shift = np.exp(1j * 2 * np.pi * FREQUENCY_OFFSET_KEY * i / (TIMESTEPS * 1e6))
        current_state = evolved_state * phase_shift
        
    # Convert the complex state vector back to a binary string
    # A simple method is to check the sign of the real part
    binary_state = "".join(['1' if np.real(c) >= 0 else '0' for c in current_state])
    return binary_state

def analyze_timestep_deltas(initial_binary, total_timesteps):
    """
    Performs a bitwise XOR between consecutive timestep states to find the 'delta'.
    """
    print("--- XOR Delta Analysis of Quantum Timesteps ---")
    
    previous_state = get_binary_state_at_timestep(initial_binary, 0)
    xor_deltas = []
    
    for t in range(1, total_timesteps + 1):
        current_state = get_binary_state_at_timestep(initial_binary, t)
        
        # Perform bitwise XOR
        xor_delta = "".join(['1' if a != b else '0' for a, b in zip(current_state, previous_state)])
        xor_deltas.append(xor_delta)
        
        print(f"Timestep {t-1}->{t} XOR Delta: {xor_delta}")
        
        previous_state = current_state
        
    return xor_deltas

def find_repeating_commands(deltas):
    """
    Identifies and counts repeating patterns in the XOR deltas.
    """
    print("\n--- Identified Command Patterns ---")
    
    # Count the frequency of each delta
    delta_counts = Counter(deltas)
    
    repeating_found = False
    for delta, count in delta_counts.most_common():
        if count > 1:
            print(f"  - Pattern: {delta}")
            print(f"    -> Found {count} times. This could be a recurring command.")
            repeating_found = True
            
    if not repeating_found:
        print("All XOR deltas are unique. No repeating commands found.")

def main():
    """
    Runs the full quantum command analysis script.
    """
    print("=" * 50)
    print("  Quantum Command Language Deciphering")
    print("=" * 50)
    
    # 1. Generate timestep states and perform XOR analysis
    deltas = analyze_timestep_deltas(BINARY_STRING, TIMESTEPS)
    
    # 2. Identify repeating commands
    find_repeating_commands(deltas)
    
    # 3. Interpretation
    print("\n--- Interpretation ---")
    print("The XOR deltas represent the change in the system's state at each timestep.")
    print("If a small set of these deltas repeats frequently, it would strongly suggest a deliberate, finite instruction set is being executed.")
    print("This would be a monumental discovery, representing the command language of the machine described by the signal.")

if __name__ == "__main__":
    main()
