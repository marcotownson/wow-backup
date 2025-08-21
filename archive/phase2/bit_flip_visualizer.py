import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import dft

# --- Constants ---
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"
TIMESTEPS = 72
FREQUENCY_OFFSET_KEY = 1420.4556
COMMAND_1 = "001110101001100100101101110000101111110011100001000110011100010011000111011110001001110000111110000011111110010011101101110100011101011101011001010110000010010101010011001000001011001011010101011100101111101000001010111010011110100100010100000110100110001011010111000110111011100001110111000110101000"

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

def create_bit_flip_map(before_state, after_state):
    """
    Creates a grid where each cell's value represents the change in a bit.
    """
    bit_flip_map = []
    for i in range(len(before_state)):
        if before_state[i] == '0' and after_state[i] == '1':
            bit_flip_map.append(10)  # New Bit
        elif before_state[i] == '1' and after_state[i] == '0':
            bit_flip_map.append(20)  # Flipped Bit
        else:
            bit_flip_map.append(0)   # Unchanged
            
    return np.array(bit_flip_map).reshape((15, 20))

def visualize_map(grid, title):
    """
    Plots the bit-flip map as a heatmap.
    """
    fig, ax = plt.subplots(figsize=(12, 9))
    cmap = plt.cm.get_cmap('viridis', 3)
    cax = ax.imshow(grid, cmap=cmap, interpolation='nearest')
    
    # Add a color bar
    cbar = fig.colorbar(cax, ticks=[0, 10, 20])
    cbar.ax.set_yticklabels(['Unchanged', 'New Bit (0->1)', 'Flipped Bit (1->0)'])
    
    ax.set_title(title)
    plt.xlabel("Bit Column")
    plt.ylabel("Bit Row")
    
    output_path = "bit_flip_heatmap.png"
    plt.savefig(output_path)
    print(f"\nBit-flip heatmap saved to '{output_path}'")
    plt.close()

def main():
    """
    Runs the bit-flip visualization script.
    """
    print("=" * 50)
    print("  Visual Deciphering of COMMAND_1")
    print("=" * 50)
    
    # 1. Get before and after states for the first occurrence of COMMAND_1
    print("Generating before and after states for Timestep 0->1...")
    before_state = get_binary_state_at_timestep(BINARY_STRING, 0)
    after_state = get_binary_state_at_timestep(BINARY_STRING, 1)
    
    # 2. Create the bit-flip map
    bit_flip_grid = create_bit_flip_map(before_state, after_state)
    
    # 3. Visualize the map
    visualize_map(bit_flip_grid, "Bit-Flip Map for COMMAND_1 (Timestep 0->1)")
    
    # 4. Interpretation
    print("\n--- Interpretation ---")
    print("The heatmap has been saved to 'bit_flip_heatmap.png'.")
    print("This visualization shows which bits are activated (0->1) and deactivated (1->0) by COMMAND_1.")
    print("If a coherent pattern emerges (e.g., a helix, a component shape, or a specific geometric form),")
    print("it would provide the final piece of evidence connecting the abstract command code to the physical blueprint of the machine.")

if __name__ == "__main__":
    main()
