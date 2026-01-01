import React from 'react';

const FixedWidthBinaryAnalyzer = () => {
  return (
    <div>
      <h2>Fixed-Width Binary Analyzer</h2>
      <p>
        This script performs a systematic analysis of the Wow! signal's binary string by
        interpreting it as a sequence of fixed-width tokens. The goal is to determine if
        the signal encodes a message using a simple, repeating binary structure, such as a
        5-bit character set.
      </p>
      <h3>Methodology</h3>
      <ol>
        <li>
          <strong>Parsing with Variable Width and Offset:</strong> The script can test any
          bit width (e.g., 5-bit, 7-bit) and, for each width, it tries every possible
          starting offset. This ensures that an aligned message is not missed.
        </li>
        <li>
          <strong>Scoring by Elemental Mapping:</strong> Each parsed token is interpreted
          as an integer and checked against the periodic table (atomic numbers 1-118).
          The script "scores" each width/offset combination by the percentage of tokens
          that map to a valid element.
        </li>
        <li>
          <strong>Reaction Motif Detection:</strong> The resulting sequence of elements is
          scanned for simple chemical patterns, or "motifs," like H₂O or NaCl.
        </li>
      </ol>
      <h3>Hypothetical 5-Bit Analysis Results</h3>
      <p>
        Given the recurring theme of a 5-bit architecture in our investigation, the 5-bit
        analysis is of particular interest. A hypothetical run of the script could yield
        the following results:
      </p>
      <pre>
        {`Fixed-width analysis | width=5
Best offset: 3 | Element-mapping rate: 28.3%
Tokens: 60
Mapped to elements: 17
Unmapped: 43
Top elements: H:4, He:3, C:2, N:2, O:2, P:1, S:1, Cl:1, Ar:1
Detected reaction motifs: 2
  @token 12: H2 → He (fusion motif)
  @token 45: H2O motif`}
      </pre>
      <h3>Interpretation</h3>
      <p>
        An element-mapping rate significantly higher than random chance (as in the
        hypothetical 28.3% above) would be strong evidence of an intentional, encoded
        message. The discovery of plausible chemical motifs, especially those related to
        fusion or the chemistry of life, would further bolster the conclusion that the
        Wow! signal is a message of profound scientific and technological importance.
      </p>
    </div>
  );
};

export default FixedWidthBinaryAnalyzer;
