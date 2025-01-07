# C-V2X Interoperability Analyzer

A Cellular Vehicle-to-Everything (C-V2X) Interoperability Analyzer based on SAE J2735 and IEEE 1609.2/1609.3 standards.

## How to Use

1. Clone this repository.

2. Ensure Python 3.12 and [PDM](https://pdm-project.org/) are installed.
   For example, using pipx:

    ```shell
    pipx install pdm
    ```

3. Run the analyzer with the target PDML file name as argument.

    ```shell
    pdm run src/cv2x-interop-analyzer.py example.pdml
    ```

4. Output is printed to stdout, but can be redirected or piped to a text file using the shell.

    ```shell
    pdm run src/cv2x-interop-analyzer.py example.pdml > output.txt
    pdm run src/cv2x-interop-analyzer.py example.pdml | tee output.txt
    ```
