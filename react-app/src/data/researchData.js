export const researchData = {
  meta: {
    project: "Wow! Signal Analysis",
    creator: "Marco Townson",
    location: "Huddersfield, West Yorkshire, HD5",
    date: "1977-08-15 (Signal), 2024-2025 (Analysis)"
  },
  hypothesis: {
    original: "6EQUJ5",
    corrected: "HEQUJ5",
    reasoning: "The intensity variation sequence '6EQUJ5' recorded by Jerry R. Ehman is hypothesized to be a transcription error. The corrected sequence 'HEQUJ5' yields coherent data when subjected to self-referential decryption."
  },
  constants: {
    binaryString: "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111",
    timeSteps: 72,
    frequencyOffset: 1420.4556,
    base: 72,
    initialBase: 34
  },
  pipeline: [
    {
      step: 1,
      title: "Self-Referential Decryption",
      description: "Converting 'HEQUJ5' using Base-72 logic derived from the signal's duration (72 seconds) to generate a 300-bit binary dataset."
    },
    {
      step: 2,
      title: "Statistical & Geometric Analysis",
      description: "Analyzing Shannon entropy, n-gram frequencies, and mapping bits to 2D bitmaps and 3D spherical coordinates."
    },
    {
      step: 3,
      title: "Quantum Evolution Modeling",
      description: "Treating the binary string as a quantum state and evolving it over 72 timesteps using Quantum Fourier Transforms (QFT)."
    },
    {
      step: 4,
      title: "Physics Modeling",
      description: "Calculating velocity, acceleration, and kinetic energy of the evolving system to identify if it behaves as a closed or open system."
    }
  ],
  findings: {
    primeNumber: true,
    chemicalMarkers: [
      { name: "H2He", significance: "Fusion Blueprint" },
      { name: "CH4", significance: "Methane (Organic Marker)" },
      { name: "H2O", significance: "Water (Universal Solvent)" }
    ],
    rosettaStone: [
      { 
        name: "ACTIVATE", 
        pattern: "00111010100110010010110111000010111111...", 
        type: "Physical Operation",
        description: "Initiates a structural or energetic change in the system."
      },
      { 
        name: "DEACTIVATE", 
        pattern: "0000101011000111011100001110111011000...", 
        type: "Physical Operation",
        description: "Resets or deactivates a component."
      },
      {
        name: "DELIMITER",
        pattern: "11111",
        type: "Syntax",
        description: "5-bit spacer identified between command sequences."
      }
    ]
  }
};