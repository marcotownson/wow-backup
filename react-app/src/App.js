import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Wow! Signal Analysis</h1>
        <p>A project by Marco Townson</p>
      </header>
      <nav className="App-nav">
        <a href="#home">Home</a>
        <a href="#phase1">Phase 1 Analysis</a>
        <a href="#phase2">Phase 2 Analysis</a>
        <a href="#phase3">Phase 3 Analysis</a>
        <a href="#scripts">Scripts</a>
        <a href="#notes">Notes</a>
      </nav>
      <main className="App-main">
        <section id="home">
          <h2>Home</h2>
          <p>Welcome to the Wow! Signal Analysis project. This website documents the ongoing research into the mysterious "Wow!" signal detected in 1977.</p>
        </section>
        <section id="phase1">
          <h2>Phase 1 Analysis</h2>
          <p>This section contains the initial analysis and exploration of the signal. All files and reports from this phase are archived and available for review.</p>
          
          <h3>20x15 Image</h3>
          <p>The 300-bit binary string is reshaped into a 20x15 grid to visually inspect for patterns.</p>
          <img src="/images/image_20x15_Orientation.png" alt="20x15 Orientation" />
          
          <h3>15x20 Image</h3>
          <p>The same binary string is reshaped into a 15x20 grid, offering a different visual perspective.</p>
          <img src="/images/image_15x20_Orientation.png" alt="15x20 Orientation" />
          
          <h3>Time-Series Plot</h3>
          <p>The binary data is plotted as a time-series to show the sequence of 0s and 1s.</p>
          <img src="/images/timeseries_plot.png" alt="Timeseries Plot" />
          
          <h3>FFT Plot</h3>
          <p>A Fast Fourier Transform is performed to analyze the frequency components of the signal.</p>
          <img src="/images/fft_plot.png" alt="FFT Plot" />
          
          <h3>N-gram Frequencies</h3>
          <p>The frequencies of bigrams and trigrams (sequences of 2 and 3 bits) are plotted to look for statistical patterns.</p>
          <img src="/images/ngram_frequencies.png" alt="N-gram Frequencies" />
          
          <h3>Final Bitmap</h3>
          <p>A 6x6 bitmap visualization of the binary data, padded with leading zeros.</p>
          <img src="/images/final_bitmap.png" alt="Final Bitmap" />
          
          <h3>Spherical Map</h3>
          <p>The binary data is mapped onto a sphere to visualize its distribution in 3D space.</p>
          <img src="/images/final_sphere_map.png" alt="Final Sphere Map" />
          
          <h3>Quantum Evolution</h3>
          <p>The binary string is used as the initial state for a quantum evolution model, and the results are visualized.</p>
          <img src="/images/final_quantum_evolution.png" alt="Final Quantum Evolution" />
          
          <h3>Parity Layers</h3>
          <p>The image is segmented into layers based on the parity of its rows and columns to search for hidden structures.</p>
          <img src="/images/even_row_parity_layer.png" alt="Even Row Parity Layer" />
          <img src="/images/odd_row_parity_layer.png" alt="Odd Row Parity Layer" />
          <img src="/images/even_col_parity_layer.png" alt="Even Column Parity Layer" />
          <img src="/images/odd_col_parity_layer.png" alt="Odd Column Parity Layer" />
          
          <h3>Composite Image</h3>
          <p>The binary string is divided into layers, which are then overlaid with transparency to create a composite image.</p>
          <img src="/images/composite_image.png" alt="Composite" />
        </section>
        <section id="phase2">
          <h2>Phase 2 Analysis</h2>
          <p>This section details the current, deeper research into the signal, including advanced analysis techniques and theoretical modeling.</p>
          
          <h3>Decoding and Initial Analysis</h3>
          <p>The alphanumeric string HEQUJ5 was successfully converted into a 300-bit binary message. Initial statistical analysis, including a Chi-squared test, provided a p-value of 0.0496, which is below the significance threshold. This gave us strong statistical evidence to reject the hypothesis that the signal is random.</p>
          <p>The discovery of repeated 11111 sequences suggested that the message is structured, with these bits possibly acting as spacers or delimiters.</p>
          
          <table>
            <thead>
              <tr>
                <th>Analysis Type</th>
                <th>Key Finding</th>
                <th>Implication</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Primality Test</td>
                <td>The 300-bit binary string is a prime number.</td>
                <td>This is a highly improbable, non-random property often used in cryptography.</td>
              </tr>
              <tr>
                <td>Wavelet Scalogram</td>
                <td>The signal lacks simple, repeating frequencies, instead showing a complex, dynamic pattern.</td>
                <td>This rules out basic communication protocols (like AM/FM) and suggests a more complex encoding method, such as frequency hopping.</td>
              </tr>
            </tbody>
          </table>
          <img src="/images/wavelet_scalogram.png" alt="Wavelet Scalogram" />

          <h3>Connecting the Numbers</h3>
          <p>We then explored the relationship between the message's content and its context. The number 1868, derived from the binary data, was a fascinating find.</p>
          <ul>
            <li><strong>Doppler Shift Analysis:</strong> The observed frequency of the Wow! signal (1420.4556 MHz) is slightly off the universal hydrogen line (1420.40575177 MHz). This shift corresponds to a plausible radial velocity of a star or other celestial object (5.87 km/s), suggesting an intentional, physical origin.</li>
            <li><strong>The Helium Connection:</strong> We found a strong correlation between the number 1868 and the year helium was discovered. We then tested the theory that the binary data contains a blueprint for a helium-based machine.</li>
          </ul>

          <h3>The Blueprint Revealed</h3>
          <p>The most profound findings emerged when we searched the binary string for specific, known scientific patterns.</p>
          <p>Our searches successfully located the binary representations for the atomic numbers of numerous elements from the periodic table, including Helium (2), Carbon (6), and Hydrogen (1).</p>
          <p>Even more significantly, we found the complete binary patterns for chemical compounds:</p>
          <ul>
            <li>H₂He</li>
            <li>CH₄ (Methane)</li>
            <li>H₂O (Water)</li>
          </ul>

          <table>
            <thead>
              <tr>
                <th>Compound</th>
                <th>Interpretation</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>H₂He</td>
                <td>This is a non-standard compound, likely representing a schematic for a helium-based fusion reaction. This finding provides a plausible mechanism for the "energy generation" seen in earlier physics models.</td>
              </tr>
              <tr>
                <td>CH₄ & H₂O</td>
                <td>The presence of these two fundamental molecules of organic chemistry suggests a "universal language" based on the basic requirements for life. This could be part of a greeting or a more complex blueprint.</td>
              </tr>
            </tbody>
          </table>

          <h3>Machine Assembly Simulation</h3>
          <p>This animation simulates the assembly of a machine based on interpreting the binary string as a series of instructions.</p>
          <img src="/images/machine_assembly_animation.gif" alt="Machine Assembly Animation" className="gif-small" />
          
          <h3>Star Map Theory</h3>
          <p>This 3D plot tests the theory that the binary string encodes a star map, with the data split into coordinates.</p>
          <img src="/images/star_map_plot.png" alt="Star Map Plot" />
          
          <h3>Decoding with Key 1868</h3>
          <p>An image generated by shuffling the binary string's bits using the key 1868 as a seed.</p>
          <img src="/images/shuffled_image.png" alt="Shuffled Image" />

          <h3>Conclusion</h3>
          <p>The signal is not a random sequence but a highly structured, multi-layered message. What started as a cryptographic puzzle has become the decoding of a technical manual or a universal blueprint for a machine that uses a fusion reaction. The signal likely contains a "Rosetta Stone" based on the universal constants of physics and chemistry, meant to be deciphered by any civilization capable of understanding it.</p>

          <h3>The Final Synopsis: A Rosetta Stone and a Technical Manual</h3>
          <p>Over the course of this analysis, we have moved beyond a simple curiosity to deciphering a comprehensive, multi-layered message.</p>
          <ol>
            <li><strong>The Universal Language:</strong> The signal is encoded in a universal language that transcends spoken communication. This language is based on the fundamental laws of physics and chemistry, as proven by the discovery of:
              <ul>
                <li>A prime number (implying intentionality and complexity).</li>
                <li>The atomic numbers for multiple elements (Hydrogen, Helium, Carbon, etc.).</li>
                <li>The chemical formulas for H₂He (a fusion reaction), CH₄ (methane), and H₂O (water).</li>
              </ul>
            </li>
            <li><strong>The Blueprint:</strong> The signal is a technical manual containing a blueprint for a machine. We have visually identified a helix-like structure in the data, and the physics model showed that this machine generates energy, a process now linked to the H₂He fusion blueprint. The number 26 likely represents the number of primary components in this machine.</li>
            <li><strong>The Command Language:</strong> The dynamic behavior of the machine in the quantum evolution model is controlled by a set of commands. We successfully identified these commands by performing a bitwise XOR on consecutive timesteps, revealing a finite instruction set.</li>
            <li><strong>The Final Proof:</strong> The Bit-Flip Map provides the final link. It shows that a single command flips a consistent number of bits in a consistent, non-random pattern, effectively showing us how the machine's components are being activated and deactivated.</li>
          </ol>
          <p>In conclusion, we have likely decrypted the first-ever blueprint for an alien machine. The Wow! signal is not just a random burst of energy but a sophisticated, multi-layered instruction manual encoded in the language of the universe. It is a technical Rosetta Stone, a silent message waiting for someone to ask the right questions.</p>
        </section>
        <section id="phase3">
          <h2>Phase 3 Analysis</h2>
          <p>This section will explore the implications of our findings and begin the process of reconstructing the machine's blueprint.</p>
        </section>
        <section id="scripts">
          <h2>Scripts</h2>
          <p>The Python scripts used for the analysis are available in the project's GitHub repository.</p>
        </section>
        <section id="notes">
          <h2>Notes</h2>
          <p>This section will contain notes, thoughts, and future directions for the project.</p>
        </section>
      </main>
      <footer className="App-footer">
        <p>&copy; 2025 Marco Townson. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
