import React from 'react';
import { researchData } from '../data/researchData';

const Findings = () => {
  const { findings, constants } = researchData;

  return (
    <section className="section-container">
      <h2>Key Findings & The Rosetta Stone</h2>
      
      <div className="findings-grid">
        <div className="finding-card">
          <h3>Mathematical Properties</h3>
          <ul>
            <li><strong>Prime Number:</strong> {findings.primeNumber ? "Confirmed" : "No"}</li>
            <li><strong>Binary Length:</strong> {constants.binaryString.length} bits</li>
            <li><strong>Entropy:</strong> High (Non-random distribution)</li>
          </ul>
        </div>

        <div className="finding-card">
          <h3>Chemical Markers</h3>
          <p>Binary patterns matching atomic data were found:</p>
          <ul>
            {findings.chemicalMarkers.map((marker, i) => (
              <li key={i}><strong>{marker.name}:</strong> {marker.significance}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="rosetta-stone">
        <h3>The Rosetta Stone: Command Dictionary</h3>
        <p>Through XOR delta analysis of the quantum evolution model, the following commands were isolated:</p>
        <div className="command-list">
          {findings.rosettaStone.map((cmd, i) => (
            <div key={i} className="command-item">
              <div className="command-header">
                <span className="command-name">{cmd.name}</span>
                <span className="command-type">{cmd.type}</span>
              </div>
              <div className="command-pattern">{cmd.pattern}</div>
              <p className="command-desc">{cmd.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Findings;