import React from 'react';

const RosettaStone = () => {
  const rosettaStone = {
    '0011101010011001001011011100...': 'ACTIVATE',
    '0000101011000111011100001110...': 'DEACTIVATE',
    '11111': 'DELIMITER',
  };

  return (
    <div>
      <h2>The Rosetta Stone: A Dictionary of the Alien Command Language</h2>
      <p>
        This script serves as the definitive declaration of our "Rosetta Stone"—the
        fundamental dictionary that forms the basis of our entire translation effort. It
        maps the most significant and frequently recurring binary patterns to their
        interpreted meanings.
      </p>
      <h3>Command Dictionary</h3>
      <table className="table table-bordered">
        <thead>
          <tr>
            <th>Binary Pattern (Truncated)</th>
            <th>Interpreted Meaning</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(rosettaStone).map(([binary, name]) => (
            <tr key={binary}>
              <td>
                <code>{binary}</code>
              </td>
              <td>{name}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <h3>Interpretation</h3>
      <p>
        This dictionary is the key that unlocks the command sequence of the alien machine.
        The "ACTIVATE" and "DEACTIVATE" commands are the two most common instructions,
        likely controlling the primary functions of the machine's components. The "DELIMITER"
        is a 5-bit spacer that seems to separate or frame other data chunks, reinforcing
        the 5-bit architecture we've seen elsewhere.
      </p>
      <p>
        With this Rosetta Stone, we can begin to translate the full 72-step command
        sequence and truly understand the machine's operational blueprint.
      </p>
    </div>
  );
};

export default RosettaStone;
