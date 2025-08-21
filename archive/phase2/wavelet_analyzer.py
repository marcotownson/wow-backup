import numpy as np
import pywt
import matplotlib.pyplot as plt

# The 300-bit binary string from the Wow! signal analysis
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"

def analyze_with_wavelets(binary_data):
    """
    Performs a wavelet analysis on the binary data to show how its frequency
    content changes over time.
    """
    print("--- Wavelet Analysis ---")
    print("Methodology: A Continuous Wavelet Transform (CWT) is applied to the signal. Unlike FFT, which provides a static frequency spectrum, the CWT shows how the frequency content evolves over the duration of the signal. This can reveal dynamic patterns, frequency shifts, or transient events.")

    # 1. Convert binary string to a numerical signal
    signal = np.array([int(bit) for bit in binary_data])

    # 2. Define wavelet and scales for the analysis
    wavelet = 'morl'  # Morlet wavelet is good for time-frequency analysis
    # A range of scales to analyze, corresponding to different frequency bands
    scales = np.arange(1, 128)

    # 3. Perform the Continuous Wavelet Transform (CWT)
    coefficients, frequencies = pywt.cwt(signal, scales, wavelet)

    # 4. Create the scalogram plot
    plt.figure(figsize=(15, 10))
    plt.imshow(np.abs(coefficients), extent=[0, 300, 1, 128], cmap='viridis', aspect='auto',
               vmax=abs(coefficients).max(), vmin=-abs(coefficients).max())
    plt.title("Wavelet Analysis (Scalogram)")
    plt.ylabel("Scale (Frequency)")
    plt.xlabel("Time (Bit Position)")
    
    # Add a colorbar to indicate the magnitude of the coefficients
    cbar = plt.colorbar()
    cbar.set_label('Coefficient Magnitude')

    # 5. Save the plot
    output_path = "wavelet_scalogram.png"
    plt.savefig(output_path)
    print(f"\n -> Wavelet scalogram saved to '{output_path}'")
    plt.close()

    # 6. Interpretation
    print("\n--- Interpretation ---")
    print("The scalogram visualizes the signal's energy at different frequencies over time.")
    print(" - Bright areas indicate high energy at a specific frequency and time.")
    print(" - Dark areas indicate low energy.")
    print("Look for horizontal bands (persistent frequencies), vertical lines (transient events), or changes in the pattern over time.")

if __name__ == "__main__":
    # First, ensure the required libraries are installed.
    try:
        import pywt
    except ImportError:
        print("PyWavelets is not installed. Please install it using: pip install PyWavelets")
    else:
        analyze_with_wavelets(BINARY_STRING)
