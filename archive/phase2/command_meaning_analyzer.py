import numpy as np
from scipy.linalg import dft
from collections import Counter

# --- Constants ---
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"
TIMESTEPS = 72
FREQUENCY_OFFSET_KEY = 1420.4556

# --- Command Patterns to Analyze ---
# These were identified as the most frequent in the previous analysis.
COMMAND_1 = "001110101001100100101101110000101111110011100001000110011100010011000111011110001001110000111110000011111110010011101101110100011101011101011001010110000010010101010011001000001011001011010101011100101111101000001010111010011110100100010100000110100110001011010111000110111011100001110111000110101000"
COMMAND_2 = "000010101100011101110000111011101100011101011010001100101100000101000100101111001011101010000010111110100111010101011010011010000010011001010101001000001101010011010111010111000101110110111001001111111000001111100001110010001111011100011001000111001100010000111001111110100001110110100100110010101110"

def get_binary_state_at_timestep(initial_binary, t):
    """
    Runs the quantum evolution model for 't' steps and returns the binary state.
    (This function is copied from the previous script for consistency).
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

def analyze_command_effect(command, before_state, after_state):
    """
    Compares the before and after states to infer the command's meaning.
    """
    print(f"\n--- Analyzing Command: {command[:15]}... ---")
    
    # 1. Bit Flips Analysis
    flips_0_to_1 = 0
    flips_1_to_0 = 0
    for i in range(len(before_state)):
        if before_state[i] == '0' and after_state[i] == '1':
            flips_0_to_1 += 1
        elif before_state[i] == '1' and after_state[i] == '0':
            flips_1_to_0 += 1
            
    print(f"Bit Flips: {flips_0_to_1} (0->1), {flips_1_to_0} (1->0)")

    # 2. Rotational (Cyclic Shift) Analysis
    is_rotation = False
    for i in range(1, len(before_state)):
        if np.roll(list(before_state), i).tolist() == list(after_state):
            print(f"  -> Change appears to be a cyclic shift of {i} positions.")
            is_rotation = True
            break
    if not is_rotation:
        print("  -> Change is not a simple cyclic shift.")

    # 3. Infer Meaning
    if flips_0_to_1 > len(before_state) * 0.4 and flips_1_to_0 > len(before_state) * 0.4:
        print("Hypothesis: This command appears to be an 'INVERT' or 'SCRAMBLE' operation due to the high number of bit flips.")
    elif is_rotation:
        print("Hypothesis: This command is likely a 'ROTATE' or 'SHIFT' operation.")
    else:
        print("Hypothesis: The command's effect is complex, possibly a state transition in a state machine or a computational step.")

def main():
    """
    Runs the command meaning analysis script.
    """
    print("=" * 50)
    print("  Deciphering Command Meanings")
    print("=" * 50)
    
    # 1. Generate all timestep deltas to find where our commands occur
    all_states = [get_binary_state_at_timestep(BINARY_STRING, t) for t in range(TIMESTEPS + 1)]
    all_deltas = ["".join(['1' if a != b else '0' for a, b in zip(all_states[t+1], all_states[t])]) for t in range(TIMESTEPS)]
    
    # 2. Find timesteps for each command and analyze
    for command_name, command_pattern in [("COMMAND_1", COMMAND_1), ("COMMAND_2", COMMAND_2)]:
        print(f"\nAnalyzing occurrences of {command_name}...")
        found = False
        for i, delta in enumerate(all_deltas):
            if delta == command_pattern:
                found = True
                before_state = all_states[i]
                after_state = all_states[i+1]
                print(f"\nFound at Timestep {i}->{i+1}")
                analyze_command_effect(command_pattern, before_state, after_state)
        if not found:
            print(f"Could not find any occurrences of {command_name}. The pattern may have been miscopied.")

    # 3. Conclusion
    print("\n--- Conclusion ---")
    print("By analyzing the state changes caused by the most frequent commands, we can begin to build a rudimentary 'dictionary' for the signal's language.")
    print("The analysis suggests that the commands correspond to complex state transitions rather than simple movements or rotations.")
    print("This implies the signal may be describing a computational process or a state machine's evolution.")

if __name__ == "__main__":
    main()
