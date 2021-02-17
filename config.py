###########################
###  System Information ###
###########################
#email for job status information
email=user+'@northeastern.edu'

#G16
g16root='/work/lopez/'
#CREST
XTBPATH='/work/lopez/xtb/'
LD_LIBRARY_PATH='"/work/lopez/orca_4_2_1_linux_x86-64_shared_openmpi216/":"/work/lopez/OpenBLAS/":$LD_LIBRARY_PATH'
#ORCA
ORCA_EXE='/work/lopez/orca_4_2_1_linux_x86-64_shared_openmpi216/'
OPENMPI='/work/lopez/openmpi-2.1.6/'

#default parition name used for utililies like the archieve feature that are moderately long ~1 day
default_partition='short'

#short partition for running really quick job steps like evaluating lowest energy conformer ~10 minutes max
short_partition='debug'

#EZTS error log directory - directory where you want to store information about calculation errors
errorlog='/scratch/neal.pa/autots-errors/'
#EZTS run log - directory where you want to store information about instances of EZTS
runlog='/scratch/neal.pa/autots-runlog/'


########################
### Input Parameters ###
########################

#This config file is designed to allow multiple tiers of benchmarking calculations. Therefore calculations with smaller basis sets 
#like 6-31G can be run with less resources than something much bigger, like aug-cc-pVTZ. The indicies of the lists for optcores and optmemory
#correspond to the different tiers. 

#The first index will be used for all calculations pre-benchmarking. If no benchmarking is requested, a list with 1 element must still be provided
# ie optcores = [8]

#OPTIMIZATIONs:
optcores=[8, 16, 16, 16]
optmemory=[60, 120, 120, 120]
optpartition="short,lopez"
optmethod="b3lyp"
optbasis="6-31G(d)"
#remeber force constants required for ts optimization
optroute="opt=(calcfc,ts,noeigen) freq=noraman"
opttime='1-00:00:00'
#the special opts keywords can be anything you want to be added to the G16 route line, so if you wanted a population analysis for example, add it here
specialopts='empiricaldispersion=GD3bj scrf=(iefpcm,solvent=water)'

#BENCHMARKING
#This section sets up the different DFT functionals, their corresponding specialopts (usually a solvent and dispersion correction if applicable)
#and breaks the basis sets up into tiers. The tiers are lists of lists of basis sets. The first list should contain the smallest basis sets
#The second list will read in the guess and force constants from the finished list 1 jobs. The third will read in the second, and so on. 
benchmarkmethods=['M11L','SVWN','SVWN5','MN12SX','M062X','M06HF','N12SX','MPWb95','PBE1PBE','PBEh1PBE','OHSE2PBE','mPW1PBE','mPW1PW91','APFD','TPSSh','B3P86','tpsskcis','B3LYP','BHandH','BMK','MPWB95','MPWPW91','bb95','wb97xd','wb97','wb97x','cam-b3lyp','LC-wHPBE']
benchmarkspecialopts=['scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water) IOp(3/76=0690003100)','scrf=(iefpcm,solvent=water) empiricaldispersion=GD3bj','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water) IOp(3/76=0870001300)','scrf=(iefpcm,solvent=water) empiricaldispersion=GD3bj','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water) empiricaldispersion=GD3bj','scrf=(iefpcm,solvent=water) IOp(3/76=0560004400)','scrf=(iefpcm,solvent=water) IOp(3/76=0572004280)','scrf=(iefpcm,solvent=water) IOp(3/76=0580004200)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water) empiricaldispersion=GD3bj','']
benchmarkbasis=[['6-31G(d)'],['6-31+G(d,p)','6-311+G(d,p)'],['cc-pvdz','aug-cc-pvdz','cc-pvtz','aug-cc-pvtz']]

#CONFORMATIONAL SEARCH:
CRESTcores=16
CRESTmem=120
CRESTtime='1-00:00:00'
CRESTpartition='short,lopez'
CRESTmethod=CRESTmethod='-xnam /work/lopez/xtb/xtb_6.2.3/bin/xtb -g H2O -ewin 500 -T 14 -opt crude -subrmsd --verbose'

ORCAmethod='B3LYP/G D3BJ 6-31G(d) def2/J NOAUTOSTART Opt cpcm(water)'
ORCAcores=8
ORCAmem=60
ORCApartition='lopez,short'
ORCAtime='1-00:00:00'


#local workflow variables
