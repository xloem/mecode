## Download an IDE
We recommend using [Visual Studio Code](https://code.visualstudio.com/)

## Confirm python is installed
In the command line or termainal run
```
python --version
```
This should output the current version of python if installed. E.g., 
```Python 3.10.9```
To download python visit [python.org/downloads](https://www.python.org/downloads/).

## Confirm git is installed
Most Mac or linux systems come with git pre-installed. To confirm if git is installed run the following in the command line on Windows or terminal on Mac:
```
git --version
```
This should output the current version of git if installed. E.g.,
```git version 2.39.2```
To download git visit [git-scm.com/downloads](https://git-scm.com/downloads).


## Configure virtual environment
=== "Conda"
    Install latest version of miniconda [https://docs.conda.io/projects/miniconda/en/latest/](https://docs.conda.io/projects/miniconda/en/latest/)

    !!! Note
        If prompted to add conda to path, the answer is almost always yes. If you're not sure, check yes to avoid `conda not found` issues down the road.

    Create a new environment for working with `mecode`. E.g., to create a virtual environment `3dp`

    ```
        conda create -n 3dp
    ```

    Once created, activate the virtual environment

    ```
        conda activate 3dp
    ```
    Using conda install pip and git 
    ```
        conda install pip git
    ```


=== "Mamba"
    Install latest version of Mamba [https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html)

    Create a new environment for working with `mecode`. E.g., to create a virtual environment `3dp`

    ```
        mamba create -n 3dp
    ```

    Once created, activate the virtual environment

    ```
        mamba activate 3dp
    ```
    Using mamba install pip and git 
    ```
        mamba install pip git
    ```

## Installing mecode
=== "GitHub"
    ```
        pip install git+https://github.com/rtellez700/mecode.git
    ```
=== "PyPi"
    In-progress
=== "Conda-Forge"
    In-progress

Open up Visual Studio Code to start you first mecode script. Run ```code .``` in the command line / terminal to open VS code for the current directory. Otherwise, open VS Code and choose the appropriate project folder. For more information on how to use VS Code please check out their documentation at [https://code.visualstudio.com/learn](https://code.visualstudio.com/learn)
