import React from 'react';
import AssemblySimulation from './phase3/AssemblySimulation';
import CommandCatalog from './phase3/CommandCatalog';
import CommandLanguageCatalog from './phase3/CommandLanguageCatalog';
import CommandSyntaxAnalyzer from './phase3/CommandSyntaxAnalyzer';
import DefinitiveTranslation from './phase3/DefinitiveTranslation';
import EquationFinder from './phase3/EquationFinder';
import FinalTranslation from './phase3/FinalTranslation';
import FixedWidthBinaryAnalyzer from './phase3/FixedWidthBinaryAnalyzer';
import HighFidelitySimulation from './phase3/HighFidelitySimulation';
import MandarinWowSignalSemanticAnalyser from './phase3/MandarinWowSignalSemanticAnalyser';
import MasterValidator from './phase3/MasterValidator';
import RosettaStone from './phase3/RosettaStone';
import WowSignalSemanticAnalyser from './phase3/WowSignalSemanticAnalyser';

const Card = ({ children }) => (
  <div className="card mb-4">
    <div className="card-body">{children}</div>
  </div>
);

const Phase3 = () => {
  return (
    <div className="container mt-4">
      <div className="text-center mb-5">
        <h1>Phase 3: Analysis and Translation</h1>
        <p className="lead">
          This phase represents the culmination of our investigation into the Wow! signal.
          It includes a deep dive into the command language, high-fidelity simulations of
          the alien machine, and a comprehensive effort to validate and translate the
          entire message.
        </p>
      </div>

      <Card>
        <RosettaStone />
      </Card>
      <Card>
        <CommandLanguageCatalog />
      </Card>
      <Card>
        <CommandSyntaxAnalyzer />
      </Card>
      <Card>
        <DefinitiveTranslation />
      </Card>
      <Card>
        <AssemblySimulation />
      </Card>
      <Card>
        <HighFidelitySimulation />
      </Card>
      <Card>
        <FinalTranslation />
      </Card>
      <Card>
        <EquationFinder />
      </Card>
      <Card>
        <FixedWidthBinaryAnalyzer />
      </Card>
      <Card>
        <WowSignalSemanticAnalyser />
      </Card>
      <Card>
        <MandarinWowSignalSemanticAnalyser />
      </Card>
      <Card>
        <MasterValidator />
      </Card>
    </div>
  );
};

export default Phase3;
