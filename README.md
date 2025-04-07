# C-V2X Interoperability Analyzer

This repository contains a software tool that is a Cellular Vehicle-to-Everything (C-V2X) interoperability
analyzer written in Python. This tool can be used to automatically parse PDML packet traces collected during
interoperability testing, analyze and assess C-V2X compatibility and interoperability among commercial On-Board
Units (OBUs) and Road-Side Units (RSUs) based on IEEE 1609.2, IEEE 1609.3, and SAE J2735 standards to achieve
and assure interoperability across devices and vendors.

## How to Use

1. Install git and Python 3.12. The installation procedure varies depending on your operating system.

    * On Debian and Ubuntu Linux, run `sudo apt install git python3-pip`.
    * On Windows, first download and install git from [here](https://git-scm.com/downloads/win), then download
      and install Python 3.12 from [here](https://www.python.org/downloads/). Make sure to select "Add python.exe
      to PATH" in the Python installer.

1. Install [PDM](https://pdm-project.org/). For example, using plain pip:

    ```shell
    pip install -U --user pdm
    ```

    Alternatively, using [pipx](https://pipx.pypa.io/stable/):

    ```shell
    pipx install pdm
    ```

    Or with [uv](https://docs.astral.sh/uv/):

    ```shell
    uv tool install pdm
    ```

    Refer to the [PDM documentation](https://pdm-project.org/en/latest/#installation) for more installation options.

1. Clone this repository.

    ```shell
    git clone https://github.com/usnistgov/C-V2XInteroperabilityAnalyzer.git
    cd C-V2XInteroperabilityAnalyzer
    ```

1. Install all required dependencies.

    ```shell
    pdm install
    ```

1. Run the analyzer with the target PDML file name as argument.

    ```shell
    pdm run src/cv2x-interop-analyzer.py example.pdml
    ```

    By default the output is printed to stdout, but can be redirected or piped to a text file using the shell.

    ```shell
    pdm run src/cv2x-interop-analyzer.py example.pdml > output.txt
    pdm run src/cv2x-interop-analyzer.py example.pdml | tee output.txt
    ```

## Contact Information

This repository is maintained by:

Eugene Songh (@eysong)

### Citation Information

You can cite this software in technical publications as:

Eugene Song (2025), C-V2X Interoperability Analyzer, National Institute of Standards and Technology, <https://doi.org/10.18434/mds2-3726>

## References

* C-V2X Interoperability Testing Datasets <https://data.nist.gov/od/id/mds2-3541>
* C-V2X Interoperability Testing Datasets: Description and Use <https://www.nist.gov/publications/c-v2x-interoperability-testing-datasets-description-and-use>
