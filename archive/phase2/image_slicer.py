import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import random

def analyze_layered_images(binary_string, num_layers, output_dir="."):
    """Creates and saves layered and composite images from a binary string."""
    print(f"\n[ANALYSIS] Generating {num_layers}-layer images...")
    print("Methodology: The 300-bit string is divided into multiple layers, which are then visualized individually and as a composite image. This could reveal hidden structures that are not apparent in a single image.")
    image_paths = []
    try:
        layer_len = len(binary_string) // num_layers
        layers = [binary_string[i:i+layer_len] for i in range(0, len(binary_string), layer_len)]
        
        composite = Image.new('RGBA', (20, 15), (0, 0, 0, 0))
        colors = [(255, 0, 0, 128), (0, 255, 0, 128), (0, 0, 255, 128), 
                  (255, 255, 0, 128), (0, 255, 255, 128), (255, 0, 255, 128)]

        for i, layer in enumerate(layers):
            if len(layer) == 300:
                pixels = np.array([int(bit) for bit in layer])
                image_grid = pixels.reshape((15, 20))
                
                plt.figure(figsize=(8, 6))
                plt.imshow(image_grid, cmap='gray_r', interpolation='nearest')
                plt.title(f"Layer {i+1}")
                path = os.path.join(output_dir, f"layer_{i+1}.png")
                plt.savefig(path)
                plt.close()
                print(f" -> Saved layer {i+1} to {path}")
                image_paths.append(path)

                layer_img = Image.new('RGBA', (20, 15), (0, 0, 0, 0))
                for y in range(15):
                    for x in range(20):
                        if image_grid[y, x] == 1:
                            layer_img.putpixel((x, y), colors[i % len(colors)])
                composite = Image.alpha_composite(composite, layer_img)

        path = os.path.join(output_dir, "composite_image.png")
        composite.save(path)
        print(f" -> Saved composite image to {path}")
        image_paths.append(path)

    except Exception as e:
        print(f"An error occurred during layered image analysis: {e}")
    return image_paths

def analyze_parity_layers(binary_string, output_dir="."):
    """Analyzes the image using bit parity to create layers."""
    print("\n[ANALYSIS] Generating parity-based image layers...")
    print("Methodology: The image is segmented into layers based on the parity (even or odd) of the number of '1's in each row and column. This can reveal hidden structures related to error-checking or data encoding schemes.")
    image_paths = []
    try:
        pixels = np.array([int(bit) for bit in binary_string])
        image_grid = pixels.reshape((15, 20))

        row_parity = np.sum(image_grid, axis=1) % 2
        col_parity = np.sum(image_grid, axis=0) % 2

        row_mask = np.tile(row_parity, (20, 1)).T
        col_mask = np.tile(col_parity, (15, 1))

        even_row_layer = image_grid * (1 - row_mask)
        odd_row_layer = image_grid * row_mask
        even_col_layer = image_grid * (1 - col_mask)
        odd_col_layer = image_grid * col_mask

        # Save the layers and collect paths
        path = os.path.join(output_dir, "even_row_parity_layer.png")
        plt.figure(figsize=(8, 6)); plt.imshow(even_row_layer, cmap='gray_r'); plt.title("Even Row Parity Layer")
        plt.savefig(path); plt.close()
        print(f" -> Saved: {path}")
        image_paths.append(path)

        path = os.path.join(output_dir, "odd_row_parity_layer.png")
        plt.figure(figsize=(8, 6)); plt.imshow(odd_row_layer, cmap='gray_r'); plt.title("Odd Row Parity Layer")
        plt.savefig(path); plt.close()
        print(f" -> Saved: {path}")
        image_paths.append(path)

        path = os.path.join(output_dir, "even_col_parity_layer.png")
        plt.figure(figsize=(8, 6)); plt.imshow(even_col_layer, cmap='gray_r'); plt.title("Even Column Parity Layer")
        plt.savefig(path); plt.close()
        print(f" -> Saved: {path}")
        image_paths.append(path)

        path = os.path.join(output_dir, "odd_col_parity_layer.png")
        plt.figure(figsize=(8, 6)); plt.imshow(odd_col_layer, cmap='gray_r'); plt.title("Odd Column Parity Layer")
        plt.savefig(path); plt.close()
        print(f" -> Saved: {path}")
        image_paths.append(path)

    except Exception as e:
        print(f"An error occurred during parity layer analysis: {e}")
    return image_paths

def analyze_with_hamming_code(binary_string, width, height, output_dir="."):
    """Demonstrates Hamming code error detection and correction."""
    print("\n[ANALYSIS] Applying Hamming Code for Error Correction...")
    print("Methodology: The binary string is encoded using Hamming codes. An error is intentionally introduced, and the code's ability to detect and correct the error is demonstrated. The original, corrupted, and corrected versions are visualized.")
    
    image_paths = {}
    try:
        if len(binary_string) != width * height:
            print(f"Error: Binary string length ({len(binary_string)}) does not match image dimensions.")
            return image_paths

        data_bits = np.array([int(b) for b in binary_string])
        n = len(data_bits)
        r = 1
        while 2**r < n + r + 1:
            r += 1
        m = n + r
        print(f" -> Encoding {n} data bits with {r} parity bits into a {m}-bit block.")

        # Encode
        encoded_bits = np.zeros(m, dtype=int)
        j = 0
        for i in range(1, m + 1):
            if (i & (i - 1)) != 0:
                if j < n:
                    encoded_bits[i-1] = data_bits[j]
                    j += 1
        for i in range(r):
            p_pos = 2**i
            parity = 0
            for j in range(1, m + 1):
                if (j & p_pos) and (encoded_bits[j-1] == 1):
                    parity ^= 1
            encoded_bits[p_pos-1] = parity

        # Visualize Original
        path = os.path.join(output_dir, "hamming_original.png")
        plt.figure(figsize=(8, 6)); plt.imshow(data_bits.reshape((height, width)), cmap='gray_r'); plt.title("Hamming: Original Data")
        plt.savefig(path); plt.close()
        print(f" -> Saved: {path}")
        image_paths['original'] = path

        # Introduce Error
        corrupted_bits = np.copy(encoded_bits)
        error_pos = random.randint(1, m)
        corrupted_bits[error_pos-1] ^= 1
        print(f" -> Intentionally introducing a single-bit error at position {error_pos}.")
        
        corrupted_data_bits = []
        for i in range(1, m + 1):
            if (i & (i - 1)) != 0:
                corrupted_data_bits.append(corrupted_bits[i-1])
        
        path = os.path.join(output_dir, "hamming_corrupted.png")
        plt.figure(figsize=(8, 6)); plt.imshow(np.array(corrupted_data_bits[:n]).reshape((height, width)), cmap='gray_r'); plt.title("Hamming: Corrupted Data")
        plt.savefig(path); plt.close()
        print(f" -> Saved: {path}")
        image_paths['corrupted'] = path

        # Check and Correct
        syndrome = 0
        for i in range(r):
            p_pos = 2**i
            parity = 0
            for j in range(1, m + 1):
                if (j & p_pos) and (corrupted_bits[j-1] == 1):
                    parity ^= 1
            if parity != 0:
                syndrome += p_pos
        
        corrected_bits = np.copy(corrupted_bits)
        if syndrome != 0:
            print(f" -> Error detected at bit position: {syndrome}. Correcting...")
            corrected_bits[syndrome-1] ^= 1
        else:
            print(" -> No error detected.")

        # Visualize Corrected
        corrected_data_bits = []
        for i in range(1, m + 1):
            if (i & (i - 1)) != 0:
                corrected_data_bits.append(corrected_bits[i-1])
        
        path = os.path.join(output_dir, "hamming_corrected.png")
        plt.figure(figsize=(8, 6)); plt.imshow(np.array(corrected_data_bits[:n]).reshape((height, width)), cmap='gray_r'); plt.title("Hamming: Corrected Data")
        plt.savefig(path); plt.close()
        print(f" -> Saved: {path}")
        image_paths['corrected'] = path

    except Exception as e:
        print(f"An error occurred during Hamming code analysis: {e}")
    return image_paths
