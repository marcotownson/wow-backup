from collections import Counter

# --- Define Core Commands ---
COMMAND_ACTIVATE = "001110101001100100101101110000101111110011100001000110011100010011000111011110001001110000111110000011111110010011101101110100011101011101011001010110000010010101010011001000001011001011010101011100101111101000001010111010011110100100010100000110100110001011010111000110111011100001110111000110101000"
COMMAND_DEACTIVATE = "000010101100011101110000111011101100011101011010001100101100000101000100101111001011101010000010111110100111010101011010011010000010011001010101001000001101010011010111010111000101110110111001001111111000001111100001110010001111011100011001000111001100010000111001111110100001110110100100110010101110"

def analyze_internal_syntax(command, command_name, chunk_size):
    """
    Analyzes the internal syntax of a command by breaking it into chunks.
    """
    print(f"\n--- Analyzing Syntax of {command_name} (Chunk Size: {chunk_size}) ---")
    
    # 1. Break into chunks
    chunks = [command[i:i+chunk_size] for i in range(0, len(command), chunk_size)]
    
    # 2. Find internal patterns (repeating chunks)
    chunk_counts = Counter(chunks)
    repeating_chunks = {chunk: count for chunk, count in chunk_counts.items() if count > 1}
    
    if repeating_chunks:
        print("Found repeating internal chunks:")
        for chunk, count in repeating_chunks.items():
            print(f"  - Chunk '{chunk}' repeated {count} times.")
    else:
        print("No repeating internal chunks found.")
        
    # 3. Check for opcode/parameter structure
    # A simple test: is the first chunk unique and the rest more repetitive?
    first_chunk = chunks[0]
    rest_chunks = chunks[1:]
    
    if chunk_counts[first_chunk] == 1 and any(count > 1 for chunk, count in Counter(rest_chunks).items()):
        print("Possible [Opcode][Parameter] structure found:")
        print(f"  - Potential Opcode: {first_chunk}")
        print("  - The rest of the command contains repeating chunks, possibly as parameters.")
    else:
        print("No obvious [Opcode][Parameter] structure found.")

def main():
    """
    Runs the command syntax analysis script.
    """
    print("=" * 50)
    print("  Command Internal Syntax Analysis")
    print("=" * 50)
    
    # Analyze both commands with different chunk sizes
    for chunk_size in [5, 8, 10]:
        analyze_internal_syntax(COMMAND_ACTIVATE, "ACTIVATE", chunk_size)
        analyze_internal_syntax(COMMAND_DEACTIVATE, "DEACTIVATE", chunk_size)
        
    # Interpretation
    print("\n" + "=" * 50)
    print("--- Interpretation of Syntax Analysis ---")
    print("This analysis attempts to find a lower-level structure within the 300-bit commands.")
    print("By breaking the commands into smaller chunks, we can look for patterns like opcodes and parameters.")
    print("Finding a consistent internal syntax would be the final piece of evidence needed to begin translating the language")
    print("and revealing the machine's full blueprint. The 5-bit chunk analysis is particularly promising due to the previously identified '11111' spacer.")

if __name__ == "__main__":
    main()
