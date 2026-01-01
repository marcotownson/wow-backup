# Wow! Signal Analysis Project

A speculative exploration into the Wow! signal by Marco Townson.

**Web Project Link:** [https://wow-backup.vercel.app/](https://wow-backup.vercel.app/)

## Overview

This project presents a deep, speculative analysis of the famous "Wow!" signal, detected in 1977. This investigation is driven by a personal hypothesis from its creator, Marco Townson.

The central premise of this entire project is that the canonical and widely cited `6EQUJ5` alphanumeric sequence was a transcription error. The analysis presented here is based on a corrected sequence: `HEQUJ5`.

Starting with this fundamental change, the project interprets the `HEQUJ5` sequence as a structured message. Through a multi-stage analysis involving statistical analysis, image generation, quantum evolution modelling, and physics simulations, the project builds a narrative that this signal contains a prime number, chemical formulas, and a blueprint for a helium-based fusion machine.

## Methodology

The analysis is performed by a suite of Python scripts, which interpret the `HEQUJ5` string in the following manner:

1.  **Binary Conversion:** The alphanumeric string `HEQUJ5` is converted into a binary data stream.
2.  **Statistical Analysis:** The binary data is subjected to various statistical tests to identify non-random patterns.
3.  **Geometric & Visual Analysis:** The data is transformed into images, parity layers, and other visual representations to search for embedded geometric patterns.
4.  **Quantum & Physics Modelling:** The binary sequence is treated as a quantum state and evolved over time. The project then models the physical properties of this evolving system.

The project's findings and the narrative derived from them are presented in a comprehensive React web application.

## Project Structure

The repository is organised as follows:

-   `archive/`: Contains the various phases of the analysis. The most current and relevant scripts are located in `archive/phase2/`.
-   `react-app/`: A React-based web application that serves as a sophisticated presentation layer for the project's narrative and findings.
-   `wow_signal_analyzer.py`: The original, monolithic analysis script.
-   `run_and_render.py`: A script that executes the analysis and generates an HTML report.
-   `validator_out/`: Contains output data from various analysis scripts.

## Web Application

The project's story, analysis, and conclusions are presented in a purpose-built web application, which can be viewed here:

[https://wow-backup.vercel.app/](https://wow-backup.vercel.app/)

The application guides the user through the different phases of the investigation, corresponding to the development of the project.

## Running the Analysis Locally

The core analysis is driven by Python.

1.  **Dependencies:** The Python scripts require several libraries. While a `requirements.txt` is present in `archive/phase1`, the most current scripts in `archive/phase2` require packages such as `numpy`, `matplotlib`, `scipy`, `gmpy2`, `reedsolo`, `tensorflow`, and `Pillow`. You will need to install these via pip.

2.  **Execution:** The main, up-to-date analysis script is `archive/phase2/consolidated_analyzer.py`. You can run it from the command line:
    ```bash
    python archive/phase2/consolidated_analyzer.py
    ```

## Disclaimer

This project is a speculative and personal exploration of the Wow! signal based on an unproven hypothesis. The conclusions presented are the result of the creator's interpretation of the analytical results and should be viewed in that context.

## Credits

This project was conceived and created by **Marco Townson**.