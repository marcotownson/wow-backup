import React from 'react';
import { researchData } from '../data/researchData';

const Hypothesis = () => {
  const { original, corrected, reasoning } = researchData.hypothesis;

  return (
    <section className="section-container">
      <h2>The Core Hypothesis</h2>
      <div className="hypothesis-card">
        <div className="comparison">
          <div className="sequence-box original">
            <h3>Original Record</h3>
            <p className="sequence">{original}</p>
            <span>Jerry R. Ehman (1977)</span>
          </div>
          <div className="arrow">➔</div>
          <div className="sequence-box corrected">
            <h3>Corrected Candidate</h3>
            <p className="sequence">{corrected}</p>
            <span>Townson Hypothesis</span>
          </div>
        </div>
        <p className="reasoning">{reasoning}</p>
      </div>
    </section>
  );
};

export default Hypothesis;