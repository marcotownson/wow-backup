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
