import React from 'react';

const AssemblySimulation = () => {
  return (
    <div>
      <h2>Assembly Simulation</h2>
      <p>
        This simulation visualizes the assembly of a machine based on a sequence of commands
        derived from a quantum model of the Wow! signal. The simulation tracks 26 components
        over 72 timesteps.
      </p>
      <h3>Simulation Logic</h3>
      <ul>
        <li>A sequence of 72 binary commands is generated.</li>
        <li>Each command is classified as a "PHYSICAL_OP" or "LOGICAL_OP".</li>
        <li>
          <strong>PHYSICAL_OP:</strong> Moves a component towards the center of the canvas,
          simulating physical assembly.
        </li>
        <li>
          <strong>LOGICAL_OP:</strong> Changes the color of a component, representing a
          change in its internal state.
        </li>
      </ul>
      <h3>Expected Outcome</h3>
      <p>
        The script is expected to generate an animation named{' '}
        <code>final_assembly_animation.gif</code>. This animation would show the components
        moving and changing color, ideally forming an organized structure over time. Due to
        execution restrictions, the animation could not be generated. However, the code
        suggests a convergence of components towards the center, with their states
        flipping between blue and red.
      </p>
      <p>
        The final animation, if generated, would be crucial for validating the "blueprint"
        theory of the Wow! signal, as it might reveal the intended structure of the
        extraterrestrial machine.
      </p>
    </div>
  );
};

export default AssemblySimulation;
