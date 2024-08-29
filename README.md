# C-V2X Interoperability Analyzer

A Cellular Vehicle-to-Everything (C-V2X) Interoperability Analyzer based on SAE J2735 and IEEE 1609.2/1609.3 standards.

## How to Use

1. Clone this repository.

2. Ensure `lxml` and `pandas` python libraries are installed.

3. Run the python script with the target pdml file name as argument.

    ```shell
    python3 C-V2XIoPAnalyzer.py example.pdml
    ```

4. Output is printed to stdout, but can be redirected or piped to a text file using the shell.

    ```shell
    python3 C-V2XIoPAnalyzer.py example.pdml > output.txt
    python3 C-V2XIoPAnalyzer.py example.pdml | tee output.txt
    ```
