# EZ-TS
Automatic Azoarene Transition State Screening

![autots-workflow](EZTS-workflow.png)

INTALLATION
    1. Copy the code to your home directory by executing the following in your home directory:
    'git clone https://github.com/lopez-lab/EZ-TS.git'
    2. Enter the autots directory, which should be at ~/EZ-TS and execute the initialization by running 'bash init.sh'. This will make the autots tools more accesible. 
    3. OpenBabel must be installed prior to use.
    4. If starting calculations from SMILES, RDKIT environment must be active.
    5. Paths to QM package executables should be set in the /home/USER/EZ-TS/config.py file.

USAGE
    SETUP
        To set up a workflow, in a directory of Gaussian log files or XYZ coordinate files simply type 'EZTS-setup' in that directory
        This will create the workflow architecture and set up all calculations with the default parameters set in /home/USER/EZ-TS/config.py*

            *You can edit the default config, or change the settings of a particular workflow by editing the config file in the /someworkflow/utilities/config.py

            To update input files in a workflow directory based on the local /someworkflow/utilities/config.py file, run 're-configure' anywhere in that workflow
            
        To set up a workflow directly from a file containing molecule SMILES, use the -s flag and provide the file name: 'EZTS-setup -s SMILES.txt'
            The SMILES.txt should have the molecule name in column1 and SMILES string in column 2:
                >Mol1       C1(/N=N/C2=CC=CC=C2)=CC=CC=C1
                >Mol2       C1(/N=N/C2=CC=CO2)=CC=CO1
                >Mol3       C1(/N=N/C2=CC=CS2)=CC=CS1
              

    RUN
        To submit the workflow simply execute the start.sh script in the base workflow directory by typing 'bash start.sh'
        This will submit three jobs: an optimization array and two dependent jobs to handle failures
        
UPDATING CODE
    To update the autots code in your home directory to the most recent version on this page, execute 'EZTS-update'.


