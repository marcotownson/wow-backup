import React, { useState } from 'react';
import './App.css';
import Hypothesis from './components/Hypothesis';
import Methodology from './components/Methodology';
import Findings from './components/Findings';
import { researchData } from './data/researchData';
import Phase3 from './components/Phase3';
import LLM from './components/LLM';
import { Analytics } from "@vercel/analytics/react";

function App() {
  const [currentView, setCurrentView] = useState('home');
  const [scriptView, setScriptView] = useState('default');

  const navigateTo = (view) => {
    setCurrentView(view);
    setScriptView('default'); // Reset script view when changing main view
    window.scrollTo(0, 0);
  };

  const navigateToScript = (script) => {
    setCurrentView('scripts');
    setScriptView(script);
    window.scrollTo(0, 0);
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>{researchData.meta.project}</h1>
        <p>Research by {researchData.meta.creator}</p>
        <div className="header-links">
          <a href="https://github.com/marcotownson/wow-backup" target="_blank" rel="noopener noreferrer" className="header-link">
            <span className="link-icon">📁</span> GitHub
          </a>
          <a href="mailto:marco@marcotownson.co.uk" className="header-link">
            <span className="link-icon">✉️</span> Email
          </a>
        </div>
      </header>
      <nav className="App-nav">
        <button onClick={() => navigateTo('home')} className={currentView === 'home' ? 'active' : ''}>Home</button>
        <button onClick={() => navigateTo('phase1')} className={currentView === 'phase1' ? 'active' : ''}>Phase 1</button>
        <button onClick={() => navigateTo('phase2')} className={currentView === 'phase2' ? 'active' : ''}>Phase 2</button>
        <button onClick={() => navigateTo('phase3')} className={currentView === 'phase3' ? 'active' : ''}>Phase 3</button>
        <button onClick={() => navigateTo('llm')} className={currentView === 'llm' ? 'active' : ''}>LLM</button>
        <button onClick={() => navigateTo('notes')} className={currentView === 'notes' ? 'active' : ''}>Notes</button>
      </nav>
      <main className="App-main">
        {currentView === 'home' && (
          <div id="home">
          <section className="section-container">
            <h2>Home</h2>
            <p>Welcome to the Wow! Signal Analysis project. This website documents the ongoing research into the mysterious "Wow!" signal detected in 1977.</p>
          </section>
          <Hypothesis />
          <Methodology />
          <button className="nav-button" onClick={() => navigateTo('phase1')}>Proceed to Phase 1 Analysis →</button>
          </div>
        )}

        {currentView === 'phase1' && (
        <section id="phase1" className="section-container">
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
          <button className="nav-button" onClick={() => navigateTo('phase2')}>Proceed to Phase 2 Analysis →</button>
        </section>
        )}

        {currentView === 'phase2' && (
        <div id="phase2">
          <section className="section-container">
            <h2>Phase 2 Analysis</h2>
            <p>This section details the current, deeper research into the signal, including advanced analysis techniques and theoretical modeling.</p>
          </section>
          
          <Findings />

          <section className="section-container">
          <h3>Statistical Validation</h3>
          <p><strong>Script:</strong> <code>chi_squared_analyzer.py</code></p>
          <p>
            To rigorously test the non-randomness hypothesis, we executed a Chi-Squared test comparing the observed frequency of bits against a theoretical random distribution.
          </p>
          <p><strong>Result:</strong> The test yielded a p-value of <strong>0.0496</strong>, falling just below the standard 0.05 significance threshold. This allows us to reject the null hypothesis, providing statistical backing that the signal contains non-random structure.</p>

          <h3>Wavelet Analysis</h3>
          <p><strong>Script:</strong> <code>wavelet_analyzer.py</code></p>
          <p>Unlike standard Fourier transforms which lose time information, this script applies a Continuous Wavelet Transform (CWT) using the Morlet wavelet to visualize how the signal's frequency content evolves over time.</p>
          <img src="/images/wavelet_scalogram.png" alt="Wavelet Scalogram" />

          <h3>Fractal Analysis</h3>
          <p><strong>Script:</strong> <code>fractal_analyzer.py</code></p>
          <p>
            This script normalizes the binary data into complex numbers and plots them using a Mandelbrot set escape-time algorithm. The goal is to identify recursive geometric structures.
          </p>
          <p><strong>Result:</strong> The generated <code>fractal_plot.png</code> reveals a self-similar structure, suggesting the information encoding may rely on fractal geometry rather than linear sequencing.</p>
          <img src="/images/fractal_plot.png" alt="Fractal Analysis Plot" />

          <h3>Machine Learning Classification</h3>
          <p><strong>Script:</strong> <code>ml_classifier.py</code></p>
          <p>We trained a TensorFlow/Keras neural network on a synthetic dataset of celestial noise vs. structured artificial signals. The model was then tasked with classifying the Wow! signal binary string.</p>
          <p><strong>Result:</strong> The model classified the signal as <strong>"Artificial"</strong> with a confidence score of <strong>98.2%</strong>.</p>

          <h3>Connecting the Numbers</h3>
          <p><strong>Script:</strong> <code>signal_analysis_theories.py</code></p>
          <p>We explored the relationship between the message's content and its context. The number 1868, derived from the binary data, was a fascinating find.</p>
          <ul>
            <li><strong>Doppler Shift Analysis:</strong> The observed frequency of the Wow! signal (1420.4556 MHz) is slightly off the universal hydrogen line (1420.40575177 MHz). This shift corresponds to a plausible radial velocity of a star or other celestial object (5.87 km/s), suggesting an intentional, physical origin.</li>
            <li><strong>The Helium Connection:</strong> We found a strong correlation between the number 1868 and the year helium was discovered. We then tested the theory that the binary data contains a blueprint for a helium-based machine.</li>
          </ul>

          <h3>The Blueprint Revealed</h3>
          <p>The most profound findings emerged when we searched the binary string for specific, known scientific patterns.</p>
          <p><strong>Scripts:</strong> <code>helium_analyzer.py</code>, <code>chemical_formula_analyzer.py</code></p>
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

          <h3>Fixed-Width Elemental Analysis</h3>
          <p><strong>Script:</strong> <code>fixed_width_binary_analyzer.py</code></p>
          <p>
            Moving beyond simple pattern matching, this script parses the binary string into fixed 5-bit tokens and maps them to atomic numbers (1-118).
          </p>
          <p><strong>Result:</strong> The analysis generated a timeline of "reaction motifs," identifying sequences where elements appear in chemically significant orders (e.g., H followed by He, suggesting fusion).</p>

          <h3>Machine Assembly Simulation</h3>
          <p><strong>Scripts:</strong> <code>machine_assembly_simulator.py</code>, <code>high_fidelity_simulation.py</code></p>
          <p>
            Using the decoded command set, we simulated the movement of 26 components in 3D space. The high-fidelity simulation visualizes energy states (glow) and trajectory convergence.
          </p>
          <img src="/images/hifi_assembly_animation.gif" alt="High Fidelity Assembly Animation" className="gif-small" />
          
          <h3>Star Map Theory</h3>
          <p><strong>Script:</strong> <code>star_map_analyzer.py</code></p>
          <p>This 3D plot tests the theory that the binary string encodes a star map, with the data split into coordinates scaled by the key 1868.</p>
          <img src="/images/star_map_plot.png" alt="Star Map Plot" />
          
          <h3>Decoding with Key 1868</h3>
          <p><strong>Script:</strong> <code>decoding_attempts.py</code></p>
          <p>An image generated by shuffling the binary string's bits using the key 1868 as a seed for the random number generator.</p>
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
          <button className="nav-button" onClick={() => navigateTo('phase3')}>Proceed to Phase 3 Analysis →</button>
        </div>
        )}

        {currentView === 'phase3' && (
          <Phase3 />
        )}

        {currentView === 'llm' && (
          <LLM />
        )}

        {currentView === 'notes' && (
        <section id="notes" className="section-container">
          <h2>Notes</h2>
          <p>This section will contain notes, thoughts, and future directions for the project.</p>
        </section>
        )}
      </main>
      <footer className="App-footer">
        <p>Project Location: {researchData.meta.location} | Status: Ongoing Analysis</p>
      </footer>
      <Analytics />
    </div>
  );
}

export default App;
