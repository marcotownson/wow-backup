import numpy as np
import matplotlib.pyplot as plt

# --- Constants ---
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"
FRACTAL_KEY = 26  # Number of iterations

def normalize_data(binary_data):
    """
    Converts the binary string into a series of complex numbers between -2.0 and 2.0.
    """
    # We need pairs of numbers for real and imaginary parts, so we'll use 20-bit chunks
    # 300 bits / 20 bits/chunk = 15 chunks
    chunk_size = 20
    chunks = [binary_data[i:i+chunk_size] for i in range(0, len(binary_data), chunk_size)]
    
    complex_numbers = []
    for chunk in chunks:
        # Split each chunk into two 10-bit parts for real and imaginary components
        real_part_bin = chunk[:10]
        imag_part_bin = chunk[10:]
        
        real_part_int = int(real_part_bin, 2)
        imag_part_int = int(imag_part_bin, 2)
        
        # Normalize to the range [-2, 2]
        # Max value for a 10-bit number is 1023
        real_part_norm = (real_part_int / 1023.0) * 4.0 - 2.0
        imag_part_norm = (imag_part_int / 1023.0) * 4.0 - 2.0
        
        complex_numbers.append(complex(real_part_norm, imag_part_norm))
        
    return complex_numbers

def generate_fractal_points(c, max_iterations):
    """
    Applies the Mandelbrot set calculation (z = z^2 + c) for a given point c.
    Returns the number of iterations it takes to 'escape'.
    """
    z = 0
    for i in range(max_iterations):
        if abs(z) > 2.0:
            return i  # Escaped
        z = z**2 + c
    return max_iterations  # Did not escape

def visualize_fractal(complex_points, max_iterations):
    """
    Plots the fractal points, colored by their escape time.
    """
    escape_times = [generate_fractal_points(c, max_iterations) for c in complex_points]
    
    x = [c.real for c in complex_points]
    y = [c.imag for c in complex_points]
    
    plt.figure(figsize=(12, 12))
    plt.scatter(x, y, c=escape_times, cmap='magma', s=100)
    plt.title(f"Fractal Plot from Binary Data (Iterations: {max_iterations})")
    plt.xlabel("Real Part")
    plt.ylabel("Imaginary Part")
    plt.colorbar(label="Escape Time (Iterations)")
    plt.grid(True)
    
    output_path = "fractal_plot.png"
    plt.savefig(output_path)
    print(f"\nFractal plot saved to '{output_path}'")
    plt.close()

def main():
    """
    Runs the fractal analysis script.
    """
    print("=" * 50)
    print("  Fractal Theory Analysis")
    print("=" * 50)
    
    # 1. Normalize data to get complex points
    complex_points = normalize_data(BINARY_STRING)
    print(f"Generated {len(complex_points)} complex points from the binary string.")
    
    # 2. Generate and visualize the fractal
    visualize_fractal(complex_points, FRACTAL_KEY)
    
    # 3. Interpretation
    print("\n--- Interpretation ---")
    print("The fractal plot has been saved to 'fractal_plot.png'.")
    print("This plot visualizes the recursive structure of the binary data when interpreted through the lens of fractal mathematics.")
    print("A symmetrical or clearly patterned output would suggest a hidden recursive structure in the signal.")
    print("Look for shapes that might resemble previously identified components, like a helix or other blueprint structures.")

if __name__ == "__main__":
    main()
