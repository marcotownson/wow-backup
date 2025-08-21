import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Constants ---
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"
NUM_OBJECTS = 26
SCALING_FACTOR = 1868

def split_data_into_chunks(binary_data, num_chunks):
    """
    Splits the binary string into a specified number of roughly equal parts.
    """
    base_len = len(binary_data) // num_chunks
    remainder = len(binary_data) % num_chunks
    
    chunks = []
    current_pos = 0
    for i in range(num_chunks):
        chunk_len = base_len + (1 if i < remainder else 0)
        chunks.append(binary_data[current_pos:current_pos + chunk_len])
        current_pos += chunk_len
    return chunks

def assign_coordinates(chunks, scale_factor):
    """
    Interprets bit chunks as 3D coordinates and scales them.
    """
    coordinates = []
    for chunk in chunks:
        n = len(chunk)
        # Divide bits for X, Y, Z. Example: 12 bits -> 4, 4, 4. 11 bits -> 4, 4, 3.
        x_bits = n // 3
        y_bits = n // 3
        z_bits = n - (x_bits + y_bits)
        
        x_bin = chunk[:x_bits]
        y_bin = chunk[x_bits:x_bits + y_bits]
        z_bin = chunk[x_bits + y_bits:]
        
        # Convert binary parts to integers
        x = int(x_bin, 2)
        y = int(y_bin, 2)
        z = int(z_bin, 2)
        
        # Normalize and apply scaling factor
        # Normalization helps to keep the coordinates in a reasonable range
        x_norm = x / (2**x_bits - 1) if x_bits > 0 else 0
        y_norm = y / (2**y_bits - 1) if y_bits > 0 else 0
        z_norm = z / (2**z_bits - 1) if z_bits > 0 else 0
        
        coordinates.append([
            x_norm * scale_factor,
            y_norm * scale_factor,
            z_norm * scale_factor
        ])
    return np.array(coordinates)

def plot_star_map(coordinates):
    """
    Creates and saves a 3D scatter plot of the coordinates.
    """
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(coordinates[:, 0], coordinates[:, 1], coordinates[:, 2], s=50, c='yellow', marker='*')
    
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_zlabel("Z Coordinate")
    ax.set_title("Hypothetical Star Map from Binary Data")
    ax.set_facecolor('black')
    
    output_path = "star_map_plot.png"
    plt.savefig(output_path)
    print(f"\n3D star map plot saved to '{output_path}'")
    plt.close()

def main():
    """
    Runs the star map analysis script.
    """
    print("=" * 50)
    print("  Star Map Theory Analysis")
    print("=" * 50)
    
    # 1. Split data into chunks
    chunks = split_data_into_chunks(BINARY_STRING, NUM_OBJECTS)
    print(f"Split data into {len(chunks)} chunks.")
    
    # 2. Assign coordinates
    coordinates = assign_coordinates(chunks, SCALING_FACTOR)
    print("Assigned and scaled 3D coordinates.")
    
    # 3. Plot the map
    plot_star_map(coordinates)
    
    # 4. Interpretation
    print("\n--- Interpretation ---")
    print("The 3D plot has been saved to 'star_map_plot.png'.")
    print("Review the plot to look for any recognizable patterns, such as:")
    print("  - A known constellation or asterism.")
    print("  - A geometric shape (e.g., a spiral, a sphere, a line).")
    print("  - A cluster of points that could represent a star system or galaxy.")
    print("Finding a non-random pattern could be strong evidence that the signal is a star map.")

if __name__ == "__main__":
    main()
