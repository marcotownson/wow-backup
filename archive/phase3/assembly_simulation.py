import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import dft
from matplotlib.animation import FuncAnimation

# --- Constants ---
BINARY_STRING = "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101160100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"
TIMESTEPS = 72
NUM_COMPONENTS = 26
FREQUENCY_OFFSET_KEY = 1420.4556

class Component:
    """Represents a single component in the machine."""
    def __init__(self, id):
        self.id = id
        self.pos = np.random.rand(2) * 20 - 10  # Start in a random [-10, 10] box
        self.color = 'blue'
        self.state = 'idle'

def get_binary_state_at_timestep(initial_binary, t):
    """Generates the binary state for a given timestep of the quantum model."""
    initial_state = np.array([int(bit) * 2 - 1 for bit in initial_binary], dtype=np.complex128)
    n = len(initial_state)
    qft_matrix = dft(n, scale='sqrtn')
    current_state = initial_state
    for i in range(t):
        evolved_state = np.dot(qft_matrix, current_state)
        phase_shift = np.exp(1j * 2 * np.pi * FREQUENCY_OFFSET_KEY * i / (TIMESTEPS * 1e6))
        current_state = evolved_state * phase_shift
    return "".join(['1' if np.real(c) >= 0 else '0' for c in current_state])

def get_command_sequence():
    """Gets the full 72-command sequence from the XOR delta analysis."""
    all_states = [get_binary_state_at_timestep(BINARY_STRING, t) for t in range(TIMESTEPS + 1)]
    return ["".join(['1' if a != b else '0' for a, b in zip(all_states[t+1], all_states[t])]) for t in range(TIMESTEPS)]

def translate_prefix_to_action(prefix):
    """Translates a command's binary prefix to a high-level action."""
    if prefix == "000":
        return "LOGICAL_OP"
    elif prefix == "001":
        return "PHYSICAL_OP"
    else:
        return "UNKNOWN_OP"

def run_simulation(commands):
    """Runs the 72-timestep simulation and returns the history of component states."""
    components = [Component(i) for i in range(NUM_COMPONENTS)]
    history = []

    for t, command in enumerate(commands):
        comp_index = t % NUM_COMPONENTS
        comp = components[comp_index]
        
        prefix = command[:3]
        action = translate_prefix_to_action(prefix)
        
        if action == "PHYSICAL_OP":
            # Move the component towards the center to simulate assembly
            comp.pos = comp.pos * 0.9
        elif action == "LOGICAL_OP":
            # Change color to represent a state change
            comp.color = 'red' if comp.color == 'blue' else 'blue'
            
        # Store the state of all components for this frame
        frame_state = [{'pos': c.pos.copy(), 'color': c.color} for c in components]
        history.append(frame_state)
        
    return history

def animate_simulation(history):
    """Creates and saves an animation of the simulation."""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.set_facecolor('black')
    
    # Initial plot
    initial_state = history[0]
    positions = np.array([s['pos'] for s in initial_state])
    colors = [s['color'] for s in initial_state]
    scatter = ax.scatter(positions[:, 0], positions[:, 1], c=colors)

    def update(frame):
        state = history[frame]
        positions = np.array([s['pos'] for s in state])
        colors = [s['color'] for s in state]
        scatter.set_offsets(positions)
        scatter.set_color(colors)
        ax.set_title(f"Assembly Simulation: Timestep {frame + 1}/{len(history)}")
        return scatter,

    anim = FuncAnimation(fig, update, frames=len(history), interval=150, blit=True)
    output_path = "final_assembly_animation.gif"
    anim.save(output_path, writer='imagemagick')
    print(f"\nAnimation saved to '{output_path}'")
    plt.close()

def main():
    print("=" * 50)
    print("  Final Assembly Simulation")
    print("=" * 50)
    
    # 1. Get the command sequence
    commands = get_command_sequence()
    
    # 2. Run the simulation
    history = run_simulation(commands)
    
    # 3. Animate the results
    animate_simulation(history)
    
    # 4. Interpretation
    print("\n" + "=" * 50)
    print("--- Interpretation ---")
    print("The simulation has been saved as 'final_assembly_animation.gif'.")
    print("This animation provides a visual representation of the machine's assembly process based on our final translation.")
    print("Observe the components for the emergence of an organized structure, such as the helix, which would validate our blueprint theory.")

if __name__ == "__main__":
    main()
