# C-V2X Interoperability Analyzer


This repository contains a software tool that is a Cellular Vehicle-to-Everything (C-V2X) Interoperability Analyzer developed using Python. This interoperability analyzer software tool can be used to automatically access testing packet datasets collected during interoperability testing, analyze and assess C-V2X compatibility and interoperability among commercial on-board units (OBUs) and road-side units (RSUs) based on IEEE 1609.2, IEEE 1609.3, and SAE J2735 standards to achieve and assure devices interoperability.


## How to Use in Linux/Unix System


1. Clone this repository.

   ```shell
   Git clone https://github.com/usnistgov/C-V2XInteroperabilityAnalyzer
   ```
   
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

    
## How to Use in Windows System (Git Bash)

Download and install the Git software on your Windows machine/laptop. This C-V2X interoperability analyzer software tool is a Python-based, developed with Python3. Python should be added to path upon installation. Below are the packages used and their versions as of development.

   ```shell
   •	lxml - 4.9.3
   •	pandas - 2.1.4
   •	time - standard
   •	re - standard
   •	sys – standard
   ```

The procedures how to setup and use C-V2X interoperability analyzer software tool are described as follows:

1)	Clone the repository from the web site: 
   
   ```shell
   Git clone https://github.com/usnistgov/C-V2XInteroperabilityAnalyzer
   ```

2)	Install python and its library.
   
   ```shell
   sudo apt-get install python3 
   python -m pip install lxml
   python -m pip install pandas
   python -m pip install datetime
   python -m pip install time
   python -m pip install re 
   python -m pip install sys
   ```

4)	Run the python script with the target pdml file name as argument.
  
   ```shell
   python C-V2XIoPAnalyzer.py exampl.pdml
   ```

5)	Run and output is printed to stdout but can be redirected or piped to a text file using the shell.
   
   ```shell
   python C-V2XIoPAnalyzer.py example.pdml > output.txt
   python C-V2XIoPAnalyzer.py example.pdml | tee output.tx
   ```


## Contact Information
This repository is maintained by:

Eugene Songh (@eysong)
Citation Information
You can cite this software in technical publications as:

Eugene Song (2025), C-V2X Interoperability Analyzer, National Institute of Standards and Technology,   https://doi.org/10.18434/mds2-3726


## References


C-V2X Interoperability Testing Datasets : https://data.nist.gov/od/id/mds2-3541 


C-V2X Interoperability Testing Datasets: Description and Use : https://www.nist.gov/publications/c-v2x-interoperability-testing-datasets-description-and-use 


