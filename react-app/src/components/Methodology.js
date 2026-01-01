import React from 'react';
import { researchData } from '../data/researchData';

const Methodology = () => {
  return (
    <section className="section-container">
      <h2>Research Methodology</h2>
      <p>
        This project employs a multi-faceted approach to analyzing the signal, moving from 
        cryptographic decryption to advanced physics simulations.
      </p>
      
      <div className="timeline">
        {researchData.pipeline.map((phase, index) => (
          <div key={index} className="timeline-item">
            <div className="timeline-marker">{phase.step}</div>
            <div className="timeline-content">
              <h3>{phase.title}</h3>
              <p>{phase.description}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="tech-stack">
        <strong>Key Technologies:</strong> Python (NumPy, SciPy, Matplotlib), Quantum Fourier Transform (QFT), Base-72 Decryption.
      </div>
    </section>
  );
};

export default Methodology;