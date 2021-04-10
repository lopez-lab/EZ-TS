from config import *
from optparse import OptionParser
import os
import sys
import numpy as np

#This script takes in a xyz coordinate file and generates a Gaussian input file

#It is used to create the initial conformer optimization inputs, the benchmarking inputs, and the final IRC inputs
#Each of these uses has a specific flag to write the correct input type

# Input Parameters


#template definitions

def generate_com(basislist,tier,name,optcores,optmemory,optmethod,optbasis,optroute,charge,multiplicity,coord,benchmarkflag,specialopts):
    coord='\n'.join(coord)
    if  benchmarkflag > -1:
        basisname=Dict[optbasis]
        with open('{0}-tier{1}.txt'.format(name,tier),'a') as coms:
            coms.write('{0}-{1}-{2}-tier{3}.com\n'.format(name,optmethod,basisname,tier))
        optroute=optroute.replace('freq=noraman','')
        optcores=optcores[tier]
        optmemory=optmemory[tier]
        if tier > 0:
            prev=tier-1
            optroute='opt=(readfc,ts,noeigen)'
            oldchk='{0}-{1}-{2}'.format(name,optmethod,Dict[basislist[tier-1]])
            script="""%oldchk={0}-tier{13}.chk
%chk={1}-{2}-{3}-tier{12}.chk
%nprocs={4}
%mem={5}GB
# {6}/{7} {8} {9} geom=check guess=read

opt

{10} {11}

--Link1--
%chk={1}-{2}-{3}-tier{12}.chk
%nprocs={4}
%mem={5}GB
# {6}/{7} {9} geom=check guess=read freq=noraman

freq

{10} {11}

""".format(oldchk,name,optmethod,basisname,optcores,optmemory,optmethod,optbasis,optroute,specialopts,charge,multiplicity,tier,prev)
        else:
            script="""%chk={0}-{1}-{2}-tier{12}.chk
%nprocs={3}
%mem={4}GB
# {5}/{6} {7} {8}

opt

{9} {10}
{11}

--Link1--
%chk={0}-{1}-{2}-tier{12}.chk
%nprocs={3}
%mem={4}GB
# {5}/{6} {8} geom=check guess=read freq=noraman

freq

{9} {10}

""".format(name,optmethod,basisname,optcores,optmemory,optmethod,optbasis,optroute,specialopts,charge,multiplicity,coord,tier)
    else:
        script="""%chk={0}.chk
%nprocs={1}
%mem={2}GB
# {3}/{4} {5} {6}

equillibrium database script

{7} {8}
{9}

""".format(name,optcores,optmemory,optmethod,optbasis,optroute,specialopts,charge,multiplicity,coord)
    return script

def Sbatch(total,p,optpartition,optcores,user,optmemory,opttime,workdir,title):
    next=p+1
    if len(title) > 20:
        tmptitle=title[0:10]
    else:
        tmptitle=title


    sbatch="""#!/bin/bash
#SBATCH --job-name={11}-tier{8}
#SBATCH --output=out.o
#SBATCH --error=out.e
#SBATCH --partition={1}
#SBATCH --nodes=1
#SBATCH --ntasks={2}
#SBATCH --mail-type=END
#SBATCH --mail-user={3}
#SBATCH --mem={4}G
#SBATCH --time={5}
#SBATCH --array=1-{10}%50
hostname
work={6}
cd $work

if [[ $SLURM_ARRAY_TASK_ID == 1 ]]
    then
    time=$(date)
    echo "$SLURM_JOB_NAME $time" >> ../status.txt

    ID=$SLURM_ARRAY_JOB_ID
    if test -f {0}-tier{9}.sbatch
        then
        echo "tier0 complete"
        sbatch --dependency=afterok:$ID {0}-tier{9}.sbatch
            fi
    sbatch --dependency=afternotok:$ID {0}-tier{8}-failed.sbatch
fi
input=$(sed "${{SLURM_ARRAY_TASK_ID}}q;d" {7}-tier{8}.txt)
export INPUT=$input
export WORKDIR=$work
export GAUSS_SCRDIR=$work
export g16root=/work/lopez/
. $g16root/g16/bsd/g16.profile
cd $WORKDIR
$g16root/g16/g16 $INPUT

station=$(grep "Station" -c ${{INPUT%.*}}.log)
if [[ $station -lt 2 ]]
    then
    exit 1234
fi

""".format(title,optpartition,optcores,user,optmemory,opttime,workdir,title,p,next,total, tmptitle)
    return sbatch

def Fixcbenchmarkopt(p,title,user,workdir,optroute,charge,multiplicity):
    next=p+1

    if len(title) > 20:
        tmptitle=title[0:10]
    else:
        tmptitle=title

    batch=r"""#!/bin/bash
#SBATCH --job-name={7}-failedbench
#SBATCH --output=resubmit.o
#SBATCH --error=resubmit.e
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --time=00:20:00
hostname

work={2}
cd $work
echo $SLURM_JOB_NAME >> ../status.txt
touch failed-script-ran

if test -f {0}-tier{3}-resubmit.txt
    then
    nresub=$(sed "1q;d" {0}-tier{3}-resubmit.txt)
else
    nresub=0
fi
nresub=$((nresub+=1))
if [[ $nresub -lt 3 ]]
    then
    rm {0}-tier{3}-resubmit.txt
    echo $nresub >> {0}-tier{3}-resubmit.txt
    for i in {0}*tier{3}.log
        do
        echo "READING FILE $i" >>{0}-resublog.txt
        finished=$(grep 'Station' -c $i)
        scf=$(grep "SCF Error SCF Error SCF Error SCF Error" $i -c )
        if [[ $finished -lt 2 ]]
            then
            convert=$(obabel $i -o xyz)
            if [[ $convert == *"0 molecules converted"* ]]
                then
                echo "${{i%.*}} did not reach restart point, or failed terribly" >> {0}-resublog.txt
                old=$(grep "%oldchk=" -c ${{i%.*}}.com)
                sed -i '1,/{4} {5}/!d' ${{i%.*}}.com
                echo " " >> ${{i%.*}}.com
                if [[ $old -gt 0 ]]
                    then
                    sed -i 1d ${{i%.*}}.com
                fi
                sed -i 's/geom=check guess=read//g' ${{i%.*}}.com
                sed -i 's/opt=(readfc,ts,noeigen)/opt=(calcfc,ts,noeigen)/g' ${{i%.*}}.com 
                tail -n +3 {0}.xyz >> ${{i%.*}}.com 
                echo " " >>  ${{i%.*}}.com
                echo '--Link1--' >>  ${{i%.*}}.com
                top=$(head -n 8 ${{i%.*}}.com)
                echo -ne "${{top/opt=(calcfc,ts,noeigen)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                echo " " >>  ${{i%.*}}.com

            #SCF Convergence issues
            elif [[ $scf -gt 0 ]]
                then
                echo "${{i%.*}} SCF failed to converge, using scf=qc" >> {0}-resublog.txt
                sed -i 's/opt/scf=qc opt/g' ${{i%.*}}.com
            else

            sed -i '1,/{4} {5}/!d' ${{i%.*}}.com
            termination=$(grep "Normal termination" -c $i)
            cycles=$(grep "SCF Done" -c $i)
            check=$(grep "geom=check guess=read" -c ${{i%.*}}.com)
            
            old=$(grep "%oldchk=" -c ${{i%.*}}.com)

            #Non stationary point found
                 #read in fc
            if [[ $finished -eq 1 ]] && [[ $termination -ge 2 ]]
                then
                echo "${{i%.*}} finished with non-stationary point, reading previous fc" >> {0}-resublog.txt
                echo " " ${{i%.*}}.com
                if [[ $old -gt 0 ]]
                    then
                    sed -i 1d ${{i%.*}}.com
                fi
                sed -i 's/geom=check guess=read//g' ${{i%.*}}.com
                mv ${{i%.*}}.chk ${{i%.*}}-readingfc.chk
                echo " " >>  ${{i%.*}}.com
                echo '--Link1--' >>  ${{i%.*}}.com
                sed -i 's/opt=(calcfc,ts,noeigen)/opt=(readfc,ts,noeigen)/g' ${{i%.*}}.com
                top=$(head -n 8 ${{i%.*}}.com)
                echo -ne "${{top/opt=(readfc,ts,noeigen)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                sed -i 's/opt=(readfc,ts,noeigen)/opt=(readfc,ts,noeigen) geom=check guess=read/g' ${{i%.*}}.com
                sed -i "1s/^/%oldchk=${{i%.*}}-readingfc.chk\n/" ${{i%.*}}.com
                echo " " >>${{i%.*}}.com
 
             #stationary found, but didnt finish frequencies or far from starting geometry
                 #re-calculate force constants
             elif ([[ $finished -eq 1 ]] && [[ $termination -lt 2 ]]) || ([[ $cycles -gt 15 ]])
                then
                echo "${{i%.*}} didnt finish freq, or is far from starting geometry" >> {0}-resublog.txt
                if [[ $old -gt 0 ]]
                    then
                    sed -i 1d ${{i%.*}}.com
                fi
                obabel $i -o xyz | tail -n +3 >> ${{i%.*}}.com
                sed -i 's/geom=check guess=read//g' ${{i%.*}}.com
                sed -i 's/opt=(readfc,ts,noeigen)/opt=(calcfc,ts,noeigen)/g' ${{i%.*}}.com
                echo " " >> ${{i%.*}}.com
                echo '--Link1--' >>  ${{i%.*}}.com
                top=$(head -n 8 ${{i%.*}}.com)
                echo -ne "${{top/opt=(calcfc,ts,noeigen)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                echo " " >>${{i%.*}}.com

             #no stationary point found yet
             else
                
                fc=$(grep "Converged?" -c $i)
  
                #if force constants were finished computing, read them
                if [[ $fc -gt 0 ]]
                    then
                    echo "${{i%.*}} no stationary point found, reading fc" >> {0}-resublog.txt
                    if [[ $old -gt 0 ]]
                        then
                        sed -i 1d ${{i%.*}}.com
                    fi
                    sed -i 's/geom=check guess=read//g' ${{i%.*}}.com
                    mv ${{i%.*}}.chk ${{i%.*}}-readingfc.chk
                    sed -i 's/opt=(calcfc,ts,noeigen)/opt=(readfc,ts,noeigen)/g' ${{i%.*}}.com
                    echo " " >> ${{i%.*}}.com
                    echo '--Link1--' >>  ${{i%.*}}.com
                    top=$(head -n 8 ${{i%.*}}.com)
                    echo -ne "${{top/opt=(readfc,ts,noeigen)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                    sed -i 's/opt=(readfc,ts,noeigen)/opt=(readfc,ts,noeigen) geom=check guess=read/g' ${{i%.*}}.com
                    sed -i "1s/^/%oldchk=${{i%.*}}-readingfc.chk\n/" ${{i%.*}}.com
                    echo " " >>${{i%.*}}.com 

                 #if not, take geometry and restart
                 else
                    echo "${{i%.*}} no stationary point found, nor fc, starting again" >> {0}-resublog.txt
                    obabel $i -o xyz |tail -n +3 >> ${{i%.*}}.com
                    if [[ $old -gt 0 ]]
                        then
                        sed -i 1d ${{i%.*}}.com
                    fi
                    sed -i 's/geom=check guess=read//g' ${{i%.*}}.com
                    sed -i 's/opt=(readfc,ts,noeigen)/opt=(calcfc,ts,noeigen)/g' ${{i%.*}}.com 
                    echo " " >>${{i%.*}}.com
                    echo '--Link1--' >>  ${{i%.*}}.com
                    top=$(head -n 8 ${{i%.*}}.com)
                    echo -ne "${{top/opt=(calcfc,ts,noeigen)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                    echo " " >>${{i%.*}}.com

                fi
            fi
            fi
        echo ${{i%.*}}.com >> {0}-tier{3}-resubmit.txt
    echo " " >> ${{i%.*}}.com
    else
        echo "$i is done" >> {0}-resublog.txt
    fi
    
    done

    toresub=$(cat {0}-tier{3}-resubmit.txt |wc -l)
    currentarray=$(sed "12q;d" {0}-tier{3}.sbatch)
    sed -i "s/$currentarray/#SBATCH --array=2-$toresub/g" {0}-tier{3}.sbatch
    sed -i "s/{0}-tier{3}.txt/{0}-tier{3}-resubmit.txt/g" {0}-tier{3}.sbatch
    ID=$(sbatch --parsable {0}-tier{3}.sbatch)
    sbatch --dependency=afternotok:$ID {0}-tier{3}-failed.sbatch

    if test -f {0}-tier{6}.sbatch
        then
        echo "tier1"
        sbatch --dependency=afterok:$ID {0}-tier{6}.sbatch
    fi
else
    echo "{0} failed too many times. RUN TERMINATED" >> ../status.txt
    echo "{0} failed too many times. RUN TERMINATED" >> /scratch/neal.pa/autots-errors/{0}
fi
""".format(title,user,workdir,p,charge,multiplicity,next,tmptitle)
    return batch


#take xyz and make com
def writeinput(basislist,tier,inputdir,basename,name,workdir,optcores,optmemory,optmethod,optbasis,optroute,specialopts,x,charge,multiplicity,benchmarkflag,user):
    #if x ==0:
    #    with open('{0}/{1}.log'.format(inputdir,basename)) as logfile:
    #        log=logfile.read().splitlines()
    #    for n,line in enumerate(log):
    #        if 'Multiplicity =' in line:
     #           charge=line.split()[2]
     #           multiplicity=line.split()[5]
   
    #need a way to get the charge and multiplicity again
    charge=0
    multiplicity=1
    coord=open('{0}.xyz'.format(name), 'r').read().splitlines()
    natom=int(coord[0])
    coord=coord[2:natom+2]
    if  runtype == 'benchmark':
        with open('{0}/{1}-{2}-{3}-tier{4}.com'.format(workdir,name,optmethod,Dict[optbasis],tier),'w') as shll:
            shll.write(generate_com(basislist,tier,name,optcores,optmemory,optmethod,optbasis,optroute,charge,multiplicity,coord,benchmarkflag,specialopts))
        return(charge,multiplicity)
    else:
        shll=open('{0}/{1}.com'.format(workdir,name),'w')
        shll.write(generate_com(basislist,tier,name,optcores,optmemory,optmethod,optbasis,optroute,charge,multiplicity,coord,benchmarkflag,specialopts))
        shll.close()



def write_benchmark():
    for x,n in enumerate(benchmarkmethods):
        for y,m in enumerate(benchmarkbasis):
            for z,o in enumerate(benchmarkbasis[y]):
                optmethod=n
                optbasis=o
                specialopts=benchmarkspecialopts[x]
                charge,multiplicity=writeinput(benchmarkbasis[y],z,inputdir,basename,name,workdir,optcores,optmemory,optmethod,optbasis,optroute,specialopts,x,charge,multiplicity,benchmarkflag,user)
    tiers=np.zeros(7)
    for n,tier in enumerate(benchmarkbasis):
        count=len(tier)
        tiers[0]=tiers[0]+1
        if count > 1:
            tiers[1]=tiers[1]+1
        if count > 2:
            tiers[2]=tiers[2]+1
        if count > 3:
            tiers[3]=tiers[3]+1
        if count > 4:
            tiers[4]=tiers[4]+1
        if count > 5:
            tiers[5]=tiers[5]+1
        if count > 6:
            tiers[6]=tiers[6]+1
        if count > 7:
            tiers[7]=tiers[7]+1

    for p,l in enumerate(tiers):
        if l > 0:
            total=int(len(benchmarkmethods)*l)
            with open('{0}/{1}-tier{2}.sbatch'.format(workdir,name,p),'w') as sbatch:
                sbatch.write(Sbatch(total,p,optpartition,optcores[p],user,optmemory[p],opttime,workdir,name))
            with open('{0}/{1}-tier{2}-failed.sbatch'.format(workdir,name,p),'w') as failed:
                failed.write(Fixcbenchmarkopt(p,name,user,workdir,optroute,charge,multiplicity))




################################################################################################################################################
#Generation Steps

def main():
    parser = OptionParser()
    
    parser.add_option('--benchmark',dest='benchmark',action="store_true", default=False)
    parser.add_option('-q','--charge',dest='charge',default=0)
    parser.add_option('-m','--mult',dest='mult',default=1)
    
    (options,args) = parser.parse_args()
   
    #input file is the first (only) positional argument
    try:
        name = args[0].split('.')[0]
    except:
        info="""
    no xyz input file was found
    """

        print(info)
        exit()
    
    benchmark = options.benchmark
    charge = options.charge
    try:
        charge = charge[0]
    except:
        pass

    mult = options.mult
    try:
        mult = mult[0]
    except:
        pass 
 
    #setup things
    workdir=os.getcwd()
    ext='com'

    #not sure these are necessary anymore
    confstring=name.find('-conf')
    rotstring=name.find('-rot')
    if confstring > -1:
        basename=name.split('-conf')[0]
    elif rotstring > -1:
        basename=name.split('-rot')[0]
    else:
        basename=name


    Dict={
    "6-31G(d)":"pople",
    "6-31+G(d,p)":"pople-plusdp",
    "6-311+G(d,p)":"pople-tz",
    "cc-pvdz":"cc-pvdz",
    "cc-pvtz":"cc-pvtz",
    "aug-cc-pvdz":"aug-cc-pvdz",
    "aug-cc-pvtz":"aug-cc-pvtz"
    }

    #actually write the files

    if benchmark:
        write_benchmark():

    else:
        x=0
        tier=False
        basislist=False 
        writeinput(basislist,tier,inputdir,basename,name,workdir,optcores[0],optmemory[0],optmethod,optbasis,optroute,specialopts,x,charge,mult,benchmarkflag,user)


if __name__ == '__main__':
    main()

