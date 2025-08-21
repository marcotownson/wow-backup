# -*- coding: utf-8 -*-
"""
Wow! Signal - Consolidated Analysis and Reporting Pipeline
---------------------------------------------------
This script consolidates all analysis and reporting functionality into a single pipeline.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from gmpy2 import mpz
from reedsolo import RSCodec
import tensorflow as tf
import requests
import json
import io
import sys
import random
import os
import math
from collections import Counter
from scipy.linalg import dft
from PIL import Image
import markdown
import base64

# Add the current directory to sys.path to allow relative imports when run as a script.
import sys
import os
sys.path.append(os.path.dirname(__file__))

# Import constants from the constants module to centralize configuration values.
import constants
# Import image slicing functions from the image_slicer module to modularize image processing.
import image_slicer

# --- Create Output Directory ---
# The output directory path is now retrieved from the constants module.
if not os.path.exists(constants.OUTPUT_DIR):
    os.makedirs(constants.OUTPUT_DIR)
    print(f"Created directory for final analysis: '{constants.OUTPUT_DIR}'")

# --- Helper Functions ---

def from_alphanum_to_decimal(alphanum):
    """Converts a single alphanumeric character to its decimal value."""
    if '0' <= alphanum <= '9':
        return int(alphanum)
    elif 'A' <= alphanum <= 'Z':
        return 10 + (ord(alphanum) - ord('A'))
    raise ValueError(f"Invalid character for base conversion: {alphanum}")

def sequence_to_decimal(sequence, base):
    """Converts a full alphanumeric sequence to a base-10 decimal integer."""
    decimal_value = 0
    power = len(sequence) - 1
    for digit in sequence:
        digit_val = from_alphanum_to_decimal(digit)
        if digit_val >= base:
            return None
        decimal_value += digit_val * (base ** power)
        power -= 1
    return decimal_value

# --- Analysis Functions ---

def analyze_as_image(binary_string, width, height, title):
    """Visualizes the binary string as a monochrome bitmap image and returns the file path."""
    print(f"\n[ANALYSIS] Generating {width}x{height} image...")
    print("Methodology: The 300-bit binary string is reshaped into a 2D grid of pixels (0=black, 1=white) to visually inspect for any non-random structures or patterns.")
    if len(binary_string) != width * height:
        print(f"Error: Binary string length ({len(binary_string)}) does not match image dimensions ({width*height}).")
        return None
    try:
        pixels = np.array([int(bit) for bit in binary_string])
        image_grid = pixels.reshape((height, width))
        plt.figure(figsize=(8, 8 * (height/width)))
        plt.imshow(image_grid, cmap='gray_r', interpolation='nearest')
        plt.title(f"Hypothesis: 2D Image Data ({title})")
        plt.xlabel("Pixel Column")
        plt.ylabel("Pixel Row")
        plt.grid(False)
        path = f"image_{title.replace(' ', '_')}.png"
        plt.savefig(path)
        print(f" -> Image '{title}' saved to {path}")
        plt.close()
        return path
    except Exception as e:
        print(f"An error occurred during image generation: {e}")
        return None

def analyze_as_timeseries(binary_string):
    """Plots the binary string as a simple time-series signal and returns the file path."""
    print("\n[ANALYSIS] Generating time-series plot...")
    print("Methodology: The binary string is plotted as a sequence of 0s and 1s over time to analyze its temporal characteristics.")
    try:
        signal = np.array([int(bit) for bit in binary_string])
        plt.figure(figsize=(15, 5))
        plt.step(range(len(signal)), signal, where='mid')
        plt.title("Hypothesis: Time-Series Signal")
        plt.xlabel("Timestep (Bit Position)")
        plt.ylabel("Amplitude (0 or 1)")
        plt.ylim(-0.1, 1.1)
        plt.grid(True, linestyle='--', alpha=0.6)
        path = "timeseries_plot.png"
        plt.savefig(path)
        print(f" -> Time-series plot saved to {path}")
        plt.close()
        return path
    except Exception as e:
        print(f"An error occurred during time-series plot generation: {e}")
        return None

def analyze_with_fft(binary_string):
    """Performs a Fast Fourier Transform on the signal and returns the file path."""
    print("\n[ANALYSIS] Performing Fast Fourier Transform (FFT)...")
    print("Methodology: The FFT is used to decompose the time-series signal into its constituent frequencies. This can reveal periodicities or hidden structures in the frequency domain.")
    print("Equation: X[k] = sum(x[n] * exp(-2j * pi * k * n / N)) for n=0 to N-1")
    try:
        signal = np.array([int(bit) for bit in binary_string])
        fft_result = fft(signal)
        frequencies = np.fft.fftfreq(len(signal))
        positive_freq_indices = frequencies > 0
        plt.figure(figsize=(15, 5))
        plt.plot(frequencies[positive_freq_indices], np.abs(fft_result[positive_freq_indices]))
        plt.title("Hypothesis: Frequency Spectrum Analysis (FFT)")
        plt.xlabel("Frequency (cycles per bitstream length)")
        plt.ylabel("Magnitude")
        plt.grid(True, linestyle='--', alpha=0.6)
        path = "fft_plot.png"
        plt.savefig(path)
        print(f" -> FFT plot saved to {path}")
        plt.close()
        return path
    except Exception as e:
        print(f"An error occurred during FFT analysis: {e}")
        return None

def miller_rabin(n, k=5):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n < p * p:
            return True
        if n % p == 0:
            return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def analyze_as_integer(binary_string):
    """Treats the binary string as a large integer and checks for primality."""
    print("\n[ANALYSIS] Analyzing as a single large integer...")
    print("Methodology: The 300-bit binary string is converted to a single large integer to test for primality. Prime numbers have unique mathematical properties and are often used in cryptography.")
    try:
        large_integer = int(binary_string, 2)
        print(f" -> Decimal Value: {large_integer}")
        print(" -> Checking for primality using Miller-Rabin test...")
        is_prime_result = miller_rabin(large_integer)
        if is_prime_result:
            print("\n*** MAJOR FINDING: The integer representation of the message is likely a PRIME NUMBER. ***")
        else:
            print("\n -> Result: The integer is NOT a prime number.")
        return is_prime_result
    except Exception as e:
        print(f"An error occurred during integer analysis: {e}")
        return None

def analyze_cryptography(binary_string):
    """Performs basic cryptanalysis on the binary string."""
    print("\n[ANALYSIS] Performing cryptanalysis...")
    print("Methodology: N-gram analysis is used to identify the frequency of short sequences of bits (bigrams and trigrams). Non-random data often exhibits patterns in n-gram frequencies.")
    try:
        bigrams = [binary_string[i:i+2] for i in range(len(binary_string)-1)]
        trigrams = [binary_string[i:i+3] for i in range(len(binary_string)-2)]
        bigram_counts = {gram: bigrams.count(gram) for gram in set(bigrams)}
        trigram_counts = {gram: trigrams.count(gram) for gram in set(trigrams)}
        
        print(" -> Bigram Frequencies:")
        for gram, count in sorted(bigram_counts.items()):
            print(f"    {gram}: {count}")
        print(" -> Trigram Frequencies:")
        for gram, count in sorted(trigram_counts.items()):
            print(f"    {gram}: {count}")
            
    except Exception as e:
        print(f"An error occurred during cryptanalysis: {e}")

def analyze_ecc(binary_string):
    """Investigates the potential application of Reed-Solomon codes."""
    print("\n[ANALYSIS] Investigating Error-Correcting Codes (ECCs)...")
    print("Methodology: This is a conceptual test to see if the signal could be a message encoded with a Reed-Solomon error-correcting code. A full analysis would require knowledge of the code's parameters.")
    try:
        # Conceptual: we don't know the parameters, but we can try a common one
        # The binary string needs to be converted to bytes
        byte_string = int(binary_string, 2).to_bytes((len(binary_string) + 7) // 8, byteorder='big')
        rsc = RSCodec(10) # 10 error correction symbols
        encoded = rsc.encode(byte_string)
        # Tamper with the message
        encoded = bytearray(encoded)
        encoded[0] = encoded[0] ^ 0xff
        decoded, _, _ = rsc.decode(encoded)
        print(" -> Conceptual Reed-Solomon decoding demonstration successful.")
    except Exception as e:
        print(f" -> Conceptual Reed-Solomon decoding failed: {e}")

def analyze_with_ml(binary_string):
    """Demonstrates a machine learning approach for pattern recognition."""
    print("\n[ANALYSIS] Applying Machine Learning for Pattern Recognition...")
    print("Methodology: A simple neural network is used to demonstrate how machine learning could be applied to find patterns in the binary data. This is a conceptual demonstration and would require a proper training dataset for a real analysis.")
    try:
        signal = np.array([int(bit) for bit in binary_string])
        # Reshape for a simple model
        data = signal.reshape(1, -1)
        
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(300,)),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(2, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        
        # This is a conceptual demonstration, so we don't have training data.
        # We'll just show the model summary and a conceptual prediction.
        print(" -> ML Model Summary:")
        model.summary()
        prediction = model.predict(data)
        print(f" -> Conceptual prediction for the signal: {prediction}")
    except Exception as e:
        print(f"An error occurred during ML analysis: {e}")

def analyze_signal_processing(binary_string):
    """Applies a low-pass filter to the binary data."""
    print("\n[ANALYSIS] Applying signal processing techniques...")
    print("Methodology: A simple low-pass filter (convolution) is applied to the binary signal to smooth it and potentially reveal underlying trends.")
    try:
        binary_data = np.array([int(bit) for bit in binary_string])
        filtered_data = np.convolve(binary_data, [1, 2, 3], mode='same')
        print(" -> Low-pass filter applied successfully.")
        print(f" -> Filtered data: {filtered_data}")
    except Exception as e:
        print(f"An error occurred during signal processing analysis: {e}")

def analyze_5bit_chunks(binary_string):
    """Analyzes the binary string by splitting it into 5-bit chunks."""
    print("\n[ANALYSIS] Analyzing 5-bit chunks...")
    print("Methodology: The 300-bit binary string is split into 5-bit chunks to check for patterns. The sequence '11111' is noted as a potential spacer or break.")
    chunks = [binary_string[i:i+5] for i in range(0, len(binary_string), 5)]
    chunk_analysis_output_lines = []
    for chunk in chunks:
        if chunk == "11111":
            line = f"-> {chunk} (potential spacer)"
        else:
            line = f"   {chunk}"
        print(line)
        chunk_analysis_output_lines.append(line)
    return "\n".join(chunk_analysis_output_lines)

def new_analysis_pipeline():
    print("="*60)
    # Use constants for the candidate string for consistency.
    print(f"--- LAUNCHING COMPREHENSIVE ANALYSIS OF CANDIDATE: {constants.WOW_ALPHANUMERIC} ---")
    print("="*60)

    # 1. DERIVE THE NEW BINARY STRING
    print("\n--- Step 1: Deriving Binary String from Base-72 Conversion ---")
    print("Methodology: The candidate string 'HEQUJ5' is treated as a number in Base-72 and converted to a binary string for analysis.")
    # Use constants for the alphanumeric string and time steps.
    decimal_val = sequence_to_decimal(constants.WOW_ALPHANUMERIC, constants.TIME_STEPS)
    binary_str = bin(decimal_val)[2:]
    print(f"'{constants.WOW_ALPHANUMERIC}' (Base-72) = {decimal_val}")
    print(f"Resulting Binary String ({len(binary_str)} bits): {binary_str}")

    # 2. STATISTICAL ANALYSIS
    print("\n--- Step 2: Statistical Analysis ---")
    print("Methodology: Basic statistical properties of the binary string are calculated, including the percentage of 1s and the Shannon entropy, which measures the randomness of the data.")
    length = len(binary_str)
    counts = Counter(binary_str)
    ones = counts.get('1', 0)
    one_percentage = ones / length
    entropy = -sum((c/length) * math.log2(c/length) for c in counts.values())
    print(f"1s Percentage: {one_percentage:.2%}")
    print(f"Shannon Entropy: {entropy:.4f} (1.0 = max randomness)")

    # 3. GEOMETRIC VISUALIZATIONS
    print("\n--- Step 3: Generating Geometric Visualizations ---")
    print("Methodology: The binary string is visualized in different geometric forms to search for patterns.")
    # Bitmap (padded to 6x6)
    padded_str = binary_str.zfill(36) # Pad with leading zeros
    pixel_data = np.array([int(bit) for bit in padded_str]).reshape((6, 6))
    plt.figure(figsize=(4, 4)); plt.imshow(pixel_data, cmap='gray_r', interpolation='nearest'); plt.title("6x6 Bitmap"); plt.xticks([]); plt.yticks([])
    # Use constants for the output directory.
    plt.savefig(os.path.join(constants.OUTPUT_DIR, "final_bitmap.png")); plt.close()
    print("  - Saved: final_bitmap.png")

    # Spherical Map
    bits = np.array([int(bit) for bit in binary_str])
    indices = np.arange(0, len(bits), dtype=float) + 0.5
    phi = np.arccos(1 - 2*indices/len(bits)); theta = np.pi * (1 + 5**0.5) * indices
    x, y, z = np.cos(theta)*np.sin(phi), np.sin(theta)*np.sin(phi), np.cos(phi)
    x, y, z = x[bits==1], y[bits==1], z[bits==1]
    fig = plt.figure(figsize=(8, 8)); ax = fig.add_subplot(111, projection='3d')
    u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
    ax.plot_wireframe(np.cos(u)*np.sin(v), np.sin(u)*np.sin(v), np.cos(v), color="gray", linewidth=0.5, alpha=0.2)
    ax.scatter(x, y, z, s=150, c='red'); ax.set_title("Spherical Map"); ax.set_axis_off()
    # Use constants for the output directory.
    plt.savefig(os.path.join(constants.OUTPUT_DIR, "final_sphere_map.png")); plt.close()
    print("  - Saved: final_sphere_map.png")

    # 4. QUANTUM EVOLUTION MODEL
    print("\n--- Step 4: Running Quantum Evolution Model ---")
    print("Methodology: The binary string is treated as the initial state of a quantum system, which is then evolved over time using a Quantum Fourier Transform (QFT). This can reveal complex, dynamic patterns.")
    initial_state = np.array([int(bit)*2-1 for bit in binary_str], dtype=np.complex128)
    n = len(initial_state)
    qft_matrix = dft(n, scale='sqrtn')
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={'projection': 'polar'})
    current_state = initial_state
    # Use constants for TIME_STEPS and FREQUENCY_OFFSET_KEY.
    for t in range(constants.TIME_STEPS):
        evolved_state = np.dot(qft_matrix, current_state)
        phase_shift = np.exp(1j * 2 * np.pi * constants.FREQUENCY_OFFSET_KEY * t / (constants.TIME_STEPS * 1e6))
        current_state = evolved_state * phase_shift
        theta = np.linspace(0, 2*np.pi, n, endpoint=False)
        radius = 1 + (t * 0.05)
        amplitudes = np.abs(current_state); phases = np.angle(current_state)
        sizes = 50 * (amplitudes / np.max(amplitudes)); colors = plt.cm.hsv((phases + np.pi)/(2*np.pi))
        ax.scatter(theta, np.full(n, radius), s=sizes, c=colors, alpha=0.8)
    ax.set_yticklabels([]); ax.set_xticklabels([]); ax.grid(True, linestyle='--', alpha=0.3)
    # Use constants for WOW_ALPHANUMERIC and TIME_STEPS.
    ax.set_title(f"Quantum Evolution of '{constants.WOW_ALPHANUMERIC}' over {constants.TIME_STEPS} Timesteps", pad=20)
    sm = plt.cm.ScalarMappable(cmap='hsv', norm=plt.Normalize(vmin=-np.pi, vmax=np.pi)); sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation='vertical', pad=0.1, label='Phase Angle (Radians)')
    cbar.set_ticks([-np.pi, 0, np.pi]); cbar.set_ticklabels(['-π', '0', '+π'])
    # Use constants for the output directory.
    plt.savefig(os.path.join(constants.OUTPUT_DIR, "final_quantum_evolution.png")); plt.close()
    print("  - Saved: final_quantum_evolution.png")

def model_system_physics():
    """
    Models the physics of the dynamic system to determine its nature.
    """
    print("="*60)
    print("--- Phase 2: Theoretical Physics Modeling ---")
    print("Methodology: This analysis treats the evolving data points from the quantum model as physical objects and calculates their velocity, acceleration, and kinetic energy. This can help determine if the system is open or closed.")

    # 1. Re-derive the binary string from the Base-72 conversion of HEQUJ5
    base72_decimal = 0
    power = len(constants.WOW_ALPHANUMERIC) - 1
    for digit in constants.WOW_ALPHANUMERIC:
        val = 0
        if '0' <= digit <= '9': val = int(digit)
        else: val = 10 + (ord(digit) - ord('A'))
        base72_decimal += val * (72 ** power)
   
    binary_str = bin(base72_decimal)[2:]
   
    # 2. Run the quantum evolution to extract trajectory data in Cartesian (x, y) coordinates
    initial_state = np.array([int(bit) * 2 - 1 for bit in binary_str], dtype=np.complex128)
    n = len(initial_state)
    qft_matrix = dft(n, scale='sqrtn')
   
    # Store trajectories as a list of (x, y) coordinates
    # Use constants for NUM_CLUSTERS_TO_TRACK.
    trajectories_cartesian = [[] for _ in range(constants.NUM_CLUSTERS_TO_TRACK)]
    current_state = initial_state
   
    print("Extracting Cartesian (x,y) trajectory data over 72 timesteps...")
    # Use constants for TIME_STEPS and FREQUENCY_OFFSET_KEY.
    for t in range(constants.TIME_STEPS):
        evolved_state = np.dot(qft_matrix, current_state)
        phase_shift = np.exp(1j * 2 * np.pi * constants.FREQUENCY_OFFSET_KEY * t / (constants.TIME_STEPS * 1e6))
        current_state = evolved_state * phase_shift
       
        amplitudes = np.abs(current_state)
        # Use constants for NUM_CLUSTERS_TO_TRACK.
        prominent_indices = np.argsort(amplitudes)[-constants.NUM_CLUSTERS_TO_TRACK:]
       
        for i in range(constants.NUM_CLUSTERS_TO_TRACK):
            idx = prominent_indices[i]
            theta = 2 * np.pi * idx / n
            radius = 1 + (t * 0.05)
            x, y = radius * np.cos(theta), radius * np.sin(theta)
            trajectories_cartesian[i].append((x, y))

    # 3. Calculate Physics: Velocity, Acceleration, and Force
    print("Calculating velocity, acceleration, and force vectors...")
    # Assume timestep dt=1 and mass m=1 for this model
    force_vectors = []
    total_kinetic_energy_over_time = []

    # Use constants for TIME_STEPS.
    for t in range(1, constants.TIME_STEPS - 1): # We need t-1, t, and t+1 to calculate acceleration
        kinetic_energy_at_t = 0
        forces_at_t = []
        # Use constants for NUM_CLUSTERS_TO_TRACK.
        for i in range(constants.NUM_CLUSTERS_TO_TRACK):
            # Get positions at three consecutive timesteps
            pos_prev = np.array(trajectories_cartesian[i][t-1])
            pos_curr = np.array(trajectories_cartesian[i][t])
            pos_next = np.array(trajectories_cartesian[i][t+1])
           
            # Calculate velocities
            vel_curr = pos_curr - pos_prev
            vel_next = pos_next - pos_curr
           
            # Calculate acceleration (change in velocity)
            acceleration = vel_next - vel_curr
           
            # Calculate force (F=ma, with m=1)
            forces_at_t.append(acceleration)
           
            # Calculate kinetic energy (0.5 * m * v^2)
            speed_sq = np.sum(vel_curr**2)
            kinetic_energy_at_t += 0.5 * speed_sq
       
        force_vectors.append(forces_at_t)
        total_kinetic_energy_over_time.append(kinetic_energy_at_t)

    # 4. Visualize the Physics
    print("Generating physics plots...")
   
    # Plot 1: Force Vectors on the Trajectories
    fig1, ax1 = plt.subplots(figsize=(12, 12))
    # Use constants for NUM_CLUSTERS_TO_TRACK.
    for i in range(constants.NUM_CLUSTERS_TO_TRACK):
        x_coords, y_coords = zip(*trajectories_cartesian[i])
        ax1.plot(x_coords, y_coords, '-', alpha=0.3)
        # Plot force vectors at several points along the trajectory
        for t_idx, force_vec in enumerate(force_vectors):
            if t_idx % 10 == 0: # Plot every 10th vector for clarity
                start_pos = trajectories_cartesian[i][t_idx+1]
                # Scale force vector for visibility
                ax1.quiver(start_pos[0], start_pos[1], force_vec[i][0], force_vec[i][1],
                           color='red', scale=1, scale_units='xy', angles='xy')
    ax1.set_title("Force Vectors Acting on Data Clusters")
    ax1.set_xlabel("X Position"); ax1.set_ylabel("Y Position"); ax1.grid(True)
    ax1.set_aspect('equal', adjustable='box')
    # Use constants for the output directory.
    filepath1 = os.path.join(constants.OUTPUT_DIR, "analysis_force_vectors.png")
    plt.savefig(filepath1); plt.close()
    print(f"  - Saved plot: analysis_force_vectors.png")

    # Plot 2: Total Kinetic Energy of the System
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(range(len(total_kinetic_energy_over_time)), total_kinetic_energy_over_time, 'o-', color='lime')
    ax2.set_title("Total Kinetic Energy of the System Over Time")
    ax2.set_xlabel("Timestep"); ax2.set_ylabel("Kinetic Energy (Arbitrary Units)")
    ax2.grid(True)
    # Use constants for the output directory.
    filepath2 = os.path.join(constants.OUTPUT_DIR, "analysis_kinetic_energy.png")
    plt.savefig(filepath2); plt.close()
    print(f"  - Saved plot: analysis_kinetic_energy.png")

    # 5. Formulate Archival Search Query
    energy_change = total_kinetic_energy_over_time[-1] - total_kinetic_energy_over_time[0]
    print("\n" + "="*60)
    print("--- Phase 2: Archival Search Formulation ---")
    print(f"Kinetic energy of the system changed by {energy_change:.2f} units over the duration.")
    print("This suggests an open system, either expending or generating energy.")
    print("\nRecommended Archival Query:")
    print("  - Search Type: High-Energy Event Correlation")
    print("  - Target Coordinates: RA 19h22m22s, Dec -27°03′")
    print("  - Time Window: 1977-08-15 23:15 to 23:18 UTC")
    print("  - Observatories: Vela satellites (Gamma-ray), HEAO-1 (X-ray), Kamiokande (Neutrino).")
    print("  - Objective: Search for any anomalous burst of gamma rays, x-rays, or neutrinos from the target coordinates within the time window of the Wow! signal.")

# --- LLM Integration ---
def ask_llama(analysis_summary, binary_string, five_bit_chunk_analysis):
    print("\n--- Contacting Llama instance for analysis ---")
    
    prompt = f"""
    I have performed a detailed analysis of the 'Wow!' signal candidate 'HEQUJ5'.
    Here is a summary of the findings and raw data:

    **Analysis Log:**
    ```
    {analysis_summary}
    ```

    **Raw Binary Data ({len(binary_string)} bits):**
    ```
    {binary_string}
    ```

    **5-bit Chunk Analysis:**
    The binary string was split into 5-bit chunks. The sequence '11111' appears to be a break or spacer.
    ```
    {five_bit_chunk_analysis}
    ```

    **Description of Visualizations:**
    - **20x15 and 15x20 Images:** The binary data was reshaped into two monochrome bitmap images. These images show a seemingly random pattern of black and white pixels.
    - **Time-Series Plot:** The binary data was plotted as a time-series signal, showing the sequence of 0s and 1s.
    - **FFT Plot:** A Fast Fourier Transform was performed on the time-series data. The resulting frequency spectrum shows the distribution of frequencies within the signal.
    - **N-gram Frequencies:** The frequencies of bigrams and trigrams in the binary data were calculated and plotted.
    - **Geometric Visualizations:** The binary data was visualized as a 6x6 bitmap and a spherical map.
    - **Quantum Evolution:** The binary data was used as the initial state for a quantum evolution model, and the results were visualized.

    Based on this comprehensive analysis, including the raw data, the 5-bit chunk analysis, and descriptions of the visualizations, what is your assessment? 
    Please provide a synopsis, highlight the most significant findings, and suggest concrete next steps for further analysis or decoding.
    Suggest analysis techniques, cryptographic methods, or any other relevant approaches that could help in understanding the nature of this signal which can be executed in python.
    """

    url = "http://127.0.0.1:11434/api/chat"
    data = {
        "model": "llama3.2:latest",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        response_data = response.json()
        llama_response = response_data['message']['content']
        print("\n--- Llama's Response ---")
        print(llama_response)
        with open("llama_response.md", "w") as f:
            f.write(llama_response)
        print("\nSaved Llama's response to llama_response.md")
    except requests.exceptions.RequestException as e:
        print(f"\nError contacting Llama instance: {e}")

# --- Main Execution ---
def main():
    """
    Runs the full decryption and analysis pipeline.
    """
    # Capture original stdout
    original_stdout = sys.stdout
    # Create a string buffer
    string_io = io.StringIO()
    # Redirect stdout to the buffer
    sys.stdout = string_io

    print("="*70)
    print("      WOW! SIGNAL - FULL DECRYPTION & ANALYSIS PIPELINE")
    print("="*70)

    # --- STAGE 1: DECRYPTION ---
    print(f"[DECRYPTION] Starting self-referential decryption...")
    # Constants are now imported from the constants module.
    print(f" -> Input Sequence: '{constants.WOW_ALPHANUMERIC}'")
    print(f" -> Initial Base: {constants.INITIAL_BASE}")

    # Use constants for initial base.
    n_decimal = sequence_to_decimal(constants.WOW_ALPHANUMERIC, constants.INITIAL_BASE)
    if n_decimal is None:
        print("ERROR: Initial conversion failed. Check sequence and base.")
        return
    print(f" -> Intermediate Decimal: {n_decimal}")

    new_base = n_decimal ** 2
    print(f" -> Calculated New Base ({n_decimal}²): {new_base}")

    # Use constants for alphanumeric string and new base.
    final_decimal = sequence_to_decimal(constants.WOW_ALPHANUMERIC, new_base)
    if final_decimal is None:
        print("ERROR: Final conversion failed unexpectedly.")
        return
   
    final_binary_message = bin(final_decimal)[2:]
    print(f" -> Final Binary Message Generated ({len(final_binary_message)} bits):\n{final_binary_message}")

    # --- STAGE 2: ANALYSIS ---
    print("\n" + "="*70)
    print("      STARTING ANALYSIS OF DECRYPTED MESSAGE")
    print("="*70)
    
    image_paths = []
   
    image_paths.append(analyze_as_image(final_binary_message, 20, 15, "20x15 Orientation"))
    image_paths.append(analyze_as_image(final_binary_message, 15, 20, "15x20 Orientation"))
    analyze_as_image(final_binary_message, 34, 34, "34x34 Orientation") # This one fails, so we don't add it
    image_paths.append(analyze_as_timeseries(final_binary_message))
    image_paths.append(analyze_with_fft(final_binary_message))
    is_prime = analyze_as_integer(final_binary_message)
    analyze_cryptography(final_binary_message)
    analyze_ecc(final_binary_message)
    analyze_with_ml(final_binary_message)
    analyze_signal_processing(final_binary_message)
    five_bit_chunk_analysis = analyze_5bit_chunks(final_binary_message)
    image_paths.extend(image_slicer.analyze_layered_images(final_binary_message, 3, constants.OUTPUT_DIR))
    image_paths.extend(image_slicer.analyze_parity_layers(final_binary_message, constants.OUTPUT_DIR))
    hamming_paths = image_slicer.analyze_with_hamming_code(final_binary_message, 20, 15, constants.OUTPUT_DIR)
    image_paths.extend(hamming_paths.values())
    
    # Run new analysis pipeline
    new_analysis_pipeline()
    
    # Run physics model
    model_system_physics()
   
    print("\n" + "="*70)
    print("--- ALL ANALYSES COMPLETE ---")
    print("="*70)

    # Restore original stdout
    sys.stdout = original_stdout
    # Get the captured output
    analysis_summary = string_io.getvalue()
    # Print the captured output to the console
    print(analysis_summary)

    # --- STAGE 3: LLM ANALYSIS ---
    ask_llama(analysis_summary, final_binary_message, five_bit_chunk_analysis)

    # --- STAGE 4: GENERATE HTML REPORT ---
    print("\n" + "="*70)
    print("      GENERATING COMPREHENSIVE HTML REPORT")
    print("="*70)
    try:
        # Convert the captured analysis summary (which is plain text/markdown-like) to HTML
        html_summary = markdown.markdown(analysis_summary)
        
        # Read the Llama's response from the markdown file
        llama_response_md_path = "llama_response.md"
        llama_response_html = ""
        if os.path.exists(llama_response_md_path):
            with open(llama_response_md_path, "r") as f:
                llama_response_markdown = f.read()
            llama_response_html = markdown.markdown(llama_response_markdown)

        # Embed images as base64 strings
        embedded_images_html = "<h2>Generated Images</h2>"
        for path in image_paths:
            if path and os.path.exists(path):
                try:
                    with open(path, "rb") as img_file:
                        b64_string = base64.b64encode(img_file.read()).decode('utf-8')
                    embedded_images_html += f'<h3>{os.path.basename(path)}</h3><img src="data:image/png;base64,{b64_string}" alt="{os.path.basename(path)}" style="max-width:100%; height:auto;"><hr>'
                except Exception as e:
                    print(f"Could not embed image {path}: {e}")
        
        # Combine into a single HTML file
        full_html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Wow! Signal Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
        pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; white-space: pre-wrap; }}
        h1, h2, h3 {{ color: #333; }}
        .analysis-section {{ margin-bottom: 30px; padding: 15px; border: 1px solid #eee; border-radius: 8px; }}
    </style>
</head>
<body>
    <h1>Wow! Signal Analysis Report</h1>
    <div class="analysis-section">
        <h2>Generated Visualizations</h2>
        {embedded_images_html}
    </div>
    <div class="analysis-section">
        <h2>Consolidated Analysis Log</h2>
        {html_summary}
    </div>
    <div class="analysis-section">
        <h2>Llama's Assessment</h2>
        {llama_response_html}
    </div>
</body>
</html>
        """
        report_path = os.path.join(constants.OUTPUT_DIR, "analysis_report.html")
        with open(report_path, "w") as f:
            f.write(full_html_content)
        print(f" -> Comprehensive HTML report saved to {report_path}")
    except Exception as e:
        print(f"An error occurred during HTML report generation: {e}")

if __name__ == "__main__":
    main()
