# C-V2XIoPAnalyzer
A Cellular-Vehicle to Everything (C-V2X) Interoperability Analyzer based on SAE J2735 and IEEE 1609.3 Standards.

## How to Use:
1. Download the C-V2XIoPAnalyzer python script and reference tables. Ensure lxml and pandas python libraries are installed.
2. In a UNIX/Bash shell, run the python script with the target pdml file name as a parameter.\
     &emsp;ex. 'python C-V2XIoPAnalyzer.py example.pdml'
4. Output is printed to stdout, but can be redirected or piped to a text file using the shell.\
     &emsp;ex. 'python C-V2XIoPAnalyzer.py example.pdml > output.txt'\
     &emsp;ex. 'python C-V2XIoPAnalyzer.py example.pdml | tee output.txt'
