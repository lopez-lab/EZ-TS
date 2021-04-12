#!/usr/bin/env python
from os.path import join
import sys
import os
import shutil
from optparse import OptionParser
import re
import fileinput
import glob

def prepare_smiles(smiles,workdir):
    import subprocess

    #messy to do this step with bash, but works for now
    cmd = 'for i in *.pdb; do charge=$(cat ${i%.*}.charge); obabel $i --addtotitle " charge=$charge" -o xyz -O ${i%.*}.xyz; rm $i; rm ${i%.*}.charge; done'
    p = subprocess.Popen(cmd, shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    o = p.stdout.read()
    if len(o) > 1:
        print(o)


def main():
    #get options
    parser = OptionParser()
    parser.add_option('--benchmark','-b', dest='benchmark',  action="store_true", help='Generate DFT benchmarking input files',default=False)
    parser.add_option('--irc','-i',dest='irc',action="store_true",help='preform IRC from final TS and optimize the lowest energy structre as reactant',default=False)
    parser.add_option('--workdir',dest='workdir',type=str,help='workdir to set up EZ-TS in',default=os.getcwd())
    parser.add_option('--smiles','-s',dest='smiles',type=str,help='set up EZ-TS from smi file',default=False)


    (options, args) = parser.parse_args()
    global frag1
    benchmark=options.benchmark
    irc=options.irc
    smiles = options.smiles
    workdir = options.workdir

    check = [smiles,workdir]
    for x,argument in enumerate(check):
        if isinstance(argument,list):
            check[x] = argument[0]
    smiles,workdir = check

    sys.path.insert(1,'{0}/utilities'.format(workdir))


    #if EZ-TS exisists in the directory, reset local workflow variables
    existing = False
    if os.path.isfile('{0}/input/ts_guess-list.txt'.format(workdir)):
        existing = True
        seen = False
        for line in fileinput.input('{0}/utilities/config.py'.format(workdir), inplace = True):
            if re.search('#local workflow variables',line):
                print(line,end='')
                seen = True
            else:
                if not seen:
                    print(line)
                    

    #copy EZ-TS scripts and add local workdir variables
    utilities_dir = '{0}/utilities'.format(workdir)
    if not os.path.isdir(utilities_dir):
        os.mkdir(utilities_dir)

    if not os.path.isfile('{0}/utilities/config.py'.format(workdir)):
        shutil.copy(os.path.expanduser('~/EZ-TS/config.py'),'{0}/utilities/config.py'.format(workdir))
    shutil.copy(os.path.expanduser('~/EZ-TS/generate_inputs.py'),'{0}/utilities/generate_inputs.py'.format(workdir))
    shutil.copy(os.path.expanduser('~/EZ-TS/get_lowest.py'),'{0}/utilities/get_lowest.py'.format(workdir))
#    shutil.copy(os.path.expanduser('~/EZ-TS/start.sh'),'{0}/start.sh'.format(workdir))
#    shutil.copy(os.path.expanduser('~/EZ-TS/xyz2com.py'),'{0}/utilities/xyz2com.py'.format(workdir))
    shutil.copy(os.path.expanduser('~/EZ-TS/orca2xyz.py'),'{0}/utilities/orca2xyz.py'.format(workdir))
    shutil.copy(os.path.expanduser('~/EZ-TS/smiles23D.py'),'{0}/utilities/smiles23D.py'.format(workdir))
    shutil.copy(os.path.expanduser('~/EZ-TS/compile_results-benchmarking.py'),'{0}/utilities/compile_results-benchmarking.py'.format(workdir)) 
    shutil.copy(os.path.expanduser('~/EZ-TS/compile_results.py'),'{0}/utilities/compile_results.py'.format(workdir))


    if smiles:
        from smiles23D import read_input,write_coord
        print('''Reading smiles from {0}

'''.format(smiles))
        allinputs = read_input(smiles)
        write_coord(allinputs)
        prepare_smiles(smiles,workdir)


    input_dir = '{0}/input'.format(workdir)
    benchmark_dir = '{0}/benchmarking'.format(workdir)
    lowest_ts_dir = '{0}/lowest_ts'.format(workdir)
    conf_opt_dir = '{0}/conf_opt'.format(workdir)
    conf_search_dir = '{0}/conf_search'.format(workdir)
    reactants_dir = '{0}/reactants'.format(workdir)
    irc_dir = '{0}/irc'.format(workdir)
    ts_guess_dir = '{0}/ts_guess'.format(workdir)
    #if doesnt already exist, set everything else up
    if not existing:
        #look for log or xyz files to run with
        types = ('*.log'.format(workdir),'*.xyz'.format(workdir))
        files = []
        for ext in types:
            files.extend(glob.glob(join(workdir,ext)))

        files = [file.split('/')[-1] for file in files]
    
        if len(files) < 1:
            error = '''

Error while setting up EZ-TS!
Can't find any log or xyz files in {0}.

If starting from SMILES, specify the smi file with the --smiles or -s option.

'''.format(workdir)
            print(error)
            exit()

        if not os.path.isdir(input_dir):
            os.mkdir(input_dir)
        if not os.path.isdir(ts_guess_dir):
            os.mkdir(ts_guess_dir)
        if not os.path.isdir(conf_search_dir):
            os.mkdir(conf_search_dir)
        if not os.path.isdir(conf_opt_dir):
            os.mkdir(conf_opt_dir)
        if not os.path.isdir(lowest_ts_dir):
            os.mkdir(lowest_ts_dir)
        if benchmark:
            if not os.path.isdir(benchmark_dir):
                os.mkdir(benchmark_dir)
        else:
            benchmark_dir = None
        if irc:
            if not os.path.isdir(irc_dir):
                os.mkdir(irc_dir)
            if not os.path.isdir(reactants_dir):
                os.mkdir(reactants_dir)
        else:
            irc_dir = None
            reactants_dir = None

        #move the input files to the input directory
        if smiles:
            shutil.move('{0}/{1}'.format(workdir,smiles),'{0}/input/{1}'.format(workdir,smiles))

        with open('{0}/input/ts_guess-list.txt'.format(workdir),'w') as guess_list:
            for file in files:
                #clean file names in case they conflict with EZ-TS
                cleanfile = file.replace('tier','TIER')
                cleanfile = cleanfile.replace('conf','CONF')
                cleanfile = cleanfile.replace('rot','ROT')
                shutil.move('{0}/{1}'.format(workdir,file),'{0}/input/{1}'.format(workdir,cleanfile))

                #make individual conf_search dirs
                if not os.path.isdir('{0}/conf_search/{1}'.format(workdir,file.split('.')[0])):
                    os.mkdir('{0}/conf_search/{1}'.format(workdir,file.split('.')[0]))
                    os.mkdir('{0}/conf_search/{1}/CREST'.format(workdir,file.split('.')[0]))
                    os.mkdir('{0}/conf_search/{1}/ORCA'.format(workdir,file.split('.')[0]))

        
            #write the geometry manipulations for generate_inputs.py
                guess_list.write('''{0}/{1} V1 175 R1   90 R2   0\n{0}/{1} V1 175 R1   90 R2 180\n{0}/{1} V1 175 R1  180 R2  90\n{0}/{1} V1 175 R1  180 R2 180\n{0}/{1} V1 175 R1  -90 R2   0\n{0}/{1} V1 175 R1  -90 R2  90\n'''.format(workdir,file))
                guess_list.write('''{0}/{1} V2 175 R1   90 R2   0\n{0}/{1} V2 175 R1   90 R2 180\n{0}/{1} V2 175 R1  180 R2  90\n{0}/{1} V2 175 R1  180 R2 180\n{0}/{1} V2 175 R1  -90 R2   0\n{0}/{1} V2 175 R1  -90 R2  90\n'''.format(workdir,file))
                     

    with open('{0}/utilities/config.py'.format(workdir), 'a') as config:
        config.write('''main_dir='{0}'
utilities_dir='{1}'
ts_guess_dir='{2}'
conf_search_dir='{3}'
lowest_ts_dir='{4}'
conf_opt_dir='{5}'
input_dir='{6}'
benchmark_dir='{7}'
irc_dir='{8}'
reactants_dir='{9}' '''.format(workdir,utilities_dir,ts_guess_dir,conf_search_dir,lowest_ts_dir,conf_opt_dir,input_dir,benchmark_dir,irc_dir,reactants_dir))

    os.chdir('{0}/input'.format(workdir))

    from generate_inputs import gen_inputs

    input = None
    input_list = 'ts_guess-list.txt'
    axis = 'A1 N'
    angles=''

    gen_inputs(input,input_list,axis,angles,benchmark,irc,utilities_dir,ts_guess_dir,conf_search_dir,lowest_ts_dir,conf_opt_dir,input_dir,benchmark_dir,irc_dir,reactants_dir)

    with open('{0}/start.sh'.format(workdir),'w') as start:
        start.write('''#!/bin/bash
cd {0}
if compgen -G "input/*log" > /dev/null
    then
    for i in input/*log
        do
        file=$(basename ${{i%.*}})
        ID=$(sbatch --parsable ts_guess/$file-submit.sbatch)
        echo "submitted autots workflow - $i"
    done
else
    for i in input/*xyz
        do
        file=$(basename ${{i%.*}})
        ID=$(sbatch --parsable ts_guess/$file-submit.sbatch)
        echo "submitted autots workflow - $i"
    done
fi
touch status.txt
'''.format(workdir))
    os.chmod('{0}/start.sh'.format(workdir),0o0777)

if __name__ == "__main__":
    main()

