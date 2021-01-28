# EZ-TS
Automatic Azoarene Transition State Screening

![autots-workflow](autots-workflow.png)

INTALLATION

    1. Copy the code to your home directory by executing the following in your home directory:
    'git clone https://github.com/lopez-lab/EZ-TS.git'

    2. Enter the autots directory, which should be at ~/EZ-TS and execute the initialization by running 'bash init.sh'. This will make the autots tools more accesible. 

USAGE

    SETUP
        To setup a workflow, in a directory of Gaussian log files, XYZ coordinate files, or containing a file of smiles strings simply type 'EZ-setup'
        This will create the workflow architecture and set up all calculations with the default parameters set in /home/USER/EZ-TS/config.py*

            *You can edit the default config, or change the settings of a particular workflow by editing the config file in the /someworkflow/utilities/config.py

            To update input files in a workflow directory based on the /someworkflow/utilities/config.py file, run 're-configure' anywhere in that workflow

    RUN
        To submit the workflow simply execute the start.sh script in the base workflow directory by typing 'bash start.sh'
        This will submit three jobs: an optimization array and two dependent jobs to handle failures
        
UPDATING CODE

    To update the autots code in your home directory to the most recent version on this page, execute 'EZTS-update'.


