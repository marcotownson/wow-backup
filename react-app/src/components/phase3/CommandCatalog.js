import React from 'react';

const CommandCatalog = () => {
  return (
    <div>
      <h2>Command Catalog</h2>
      <p>
        This script catalogs the commands derived from the Wow! signal, comparing them
        against a "Rosetta Stone" of known commands to identify new, unknown instructions.
      </p>
      <h3>Methodology</h3>
      <ol>
        <li>
          <strong>Generate Command Sequence:</strong> The same 72-timestep command sequence
          from the assembly simulation is generated.
        </li>
        <li>
          <strong>Identify Known Commands:</strong> The script uses two known commands, "ACTIVATE"
          and "DEACTIVATE", as a baseline.
        </li>
        <li>
          <strong>Catalog Unknown Commands:</strong> Any command in the sequence that does not
          match the known commands is cataloged and its frequency is counted.
        </li>
        <li>
          <strong>Cluster by Prefix:</strong> Unknown commands are grouped by their 3-bit
          prefix to find patterns.
        </li>
      </ol>
      <h3>Hypothetical Results</h3>
      <p>
        Due to execution restrictions, the script could not be run. However, we can
        hypothesize the outcome based on the script's design. The analysis would likely
        reveal a small number of unique unknown commands, suggesting a highly efficient
        and elegant command language.
      </p>
      <h4>Example Output:</h4>
      <pre>
        {`--- Catalog of Unknown Commands ---
- Command: 01011010... (Found 8 time(s))
- Command: 10100101... (Found 5 time(s))
- Command: 11100011... (Found 3 time(s))

--- Command Clustering (by 3-bit prefix) ---
Cluster with prefix '010':
  - 01011010...
Cluster with prefix '101':
  - 10100101...
Cluster with prefix '111':
  - 11100011...

--- Interpretation ---
Found 3 unique unknown commands...
The number of unique commands is very small, suggesting an elegant and simple language.`}
      </pre>
    </div>
  );
};

export default CommandCatalog;
