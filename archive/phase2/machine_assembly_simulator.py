import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Constants ---
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"
NUM_COMPONENTS = 26

# --- Instruction Set ---
# A simple mapping from 5-bit chunks to instructions
INSTRUCTION_SET = {
    "00000": "DEACTIVATE", "00001": "MOVE_UP", "00010": "MOVE_DOWN",
    "00011": "MOVE_LEFT", "00100": "MOVE_RIGHT", "00101": "ATTACH",
    "00110": "DETACH", "00111": "ROTATE_CW", "01000": "ROTATE_CCW",
    "11111": "WAIT"
    # Add more mappings as needed, for now, unassigned codes will be 'WAIT'
}

class Component:
    def __init__(self, id):
        self.id = id
        self.pos = np.random.rand(2) * 10  # Random starting position in a 10x10 grid
        self.active = True
        self.attached_to = None

def parse_instructions(binary_data):
    """Parses the binary string into a list of instructions."""
    chunks = [binary_data[i:i+5] for i in range(0, len(binary_data), 5)]
    return [INSTRUCTION_SET.get(chunk, "WAIT") for chunk in chunks]

def simulate_assembly(instructions):
    """Simulates the assembly process and returns the history of component positions."""
    components = [Component(i) for i in range(NUM_COMPONENTS)]
    history = []

    for i, instruction in enumerate(instructions):
        comp_index = i % NUM_COMPONENTS
        comp = components[comp_index]

        if not comp.active:
            # Record current state and continue
            current_positions = np.array([c.pos for c in components])
            history.append(current_positions)
            continue

        if instruction == "MOVE_UP":
            comp.pos[1] += 1
        elif instruction == "MOVE_DOWN":
            comp.pos[1] -= 1
        elif instruction == "MOVE_LEFT":
            comp.pos[0] -= 1
        elif instruction == "MOVE_RIGHT":
            comp.pos[0] += 1
        elif instruction == "ATTACH":
            # Attach to the nearest active, unattached component
            min_dist = float('inf')
            target = None
            for other_comp in components:
                if other_comp.id != comp.id and other_comp.active and other_comp.attached_to is None:
                    dist = np.linalg.norm(comp.pos - other_comp.pos)
                    if dist < min_dist:
                        min_dist = dist
                        target = other_comp
            if target:
                comp.attached_to = target.id
                comp.pos = target.pos + np.array([0.5, 0.5]) # Snap to target
        elif instruction == "DEACTIVATE":
            comp.active = False
        
        # Record the state of all components after this step
        current_positions = np.array([c.pos for c in components])
        history.append(current_positions)
        
    return history

def animate_simulation(history):
    """Creates and saves an animation of the assembly process."""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 15)
    
    scatter = ax.scatter(history[0][:, 0], history[0][:, 1])

    def update(frame):
        scatter.set_offsets(history[frame])
        ax.set_title(f"Assembly Simulation: Step {frame + 1}/{len(history)}")
        return scatter,

    anim = FuncAnimation(fig, update, frames=len(history), interval=100, blit=True)
    
    output_path = "machine_assembly_animation.gif"
    anim.save(output_path, writer='imagemagick')
    print(f"\nAnimation saved to '{output_path}'")
    plt.close()

def main():
    print("=" * 50)
    print("  Machine Assembly Simulation")
    print("=" * 50)
    
    # 1. Parse instructions
    instructions = parse_instructions(BINARY_STRING)
    print(f"Parsed {len(instructions)} instructions.")
    
    # 2. Run simulation
    print("Running simulation...")
    history = simulate_assembly(instructions)
    
    # 3. Create animation
    print("Creating animation...")
    animate_simulation(history)
    
    # 4. Interpretation
    print("\n--- Interpretation ---")
    print("The simulation has been animated and saved to 'machine_assembly_animation.gif'.")
    print("Review the animation to see if the components assemble into a coherent or functional-looking object.")
    print("If a structured object is formed, it would strongly support the theory that the binary string contains assembly instructions.")

if __name__ == "__main__":
    main()
