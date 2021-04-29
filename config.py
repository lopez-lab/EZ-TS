###########################
###  System Information ###
###########################
sys_user='neal.pa'
#email for job status information
user=sys_user+'@northeastern.edu'

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
errorlog='~/EZ-TS/errors/'
#EZTS run log - directory where you want to store information about instances of EZ-TS
runlog='~/EZ-TS/runlog/'


########################
### Input Parameters ###
########################

#This config file is designed to allow multiple tiers of benchmarking calculations. Therefore calculations with smaller basis sets 
#like 6-31G can be run with less resources than something much bigger, like aug-cc-pVTZ, and the lowerbasis guess structure/force constansts
#can be read into hier tier calculations. 
#The indicies of the lists correspond with the tier. The tiers are defined in the 'benchmarkbasis' where each list is a series of basis sets
# to read from eachother. For example, to scale up the correlation consistent basis set ladder ['cc-pvdz','aug-cc-pvdz','aug-cc-pvtz'] 
#defines tier0 as cc-pvdz
#        tier1 as aug-cc-pvdz (reading guess from tier0)
#        tier2 as aug-cc-pvtz (reading guess from tier1)


#The first index will be used for all calculations pre-benchmarking. If no benchmarking is requested, a list with 1 element must still be provided
# ie optcores = [8]

#OPTIMIZATIONs:
optcores=[16, 32, 32, 32]
optmemory=[120, 240, 240, 240]
optpartition="short,lopez"
optmethod="b3lyp"
optbasis="6-31G(d)"
#remeber force constants required for ts optimization
#lowering max step in the ts_guess to minimize optimizing away from a good TS
ts_guessroute="opt=(calcfc,ts,noeigen,maxstep=10) freq=noraman"
optroute="opt=(calcfc,ts,noeigen) freq=noraman"
optroute_reactants="opt freq=noraman"
ircroute_forward="IRC=(forward,rcfc,maxpoints=20,recorrect=never) geom=check guess=read"
ircroute_reverse="IRC=(reverse,rcfc,maxpoints=20,recorrect=never) geom=check guess=read"
opttime='1-00:00:00'
#the special opts keywords can be anything you want to be added to the G16 route line, so if you wanted a population analysis for example, add it here
specialopts='empiricaldispersion=GD3bj scrf=(iefpcm,solvent=water)'

#BENCHMARKING
benchmarkmethods=[['M11L','scrf=(iefpcm,solvent=water)'],['SVWN','scrf=(iefpcm,solvent=water)'],['SVWN5','scrf=(iefpcm,solvent=water)'],['MN12SX','scrf=(iefpcm,solvent=water)'],['M062X','scrf=(iefpcm,solvent=water)'],['M06HF','scrf=(iefpcm,solvent=water)'],['N12SX','scrf=(iefpcm,solvent=water)'],['MPWb95','scrf=(iefpcm,solvent=water) IOp(3/76=0690003100)'],['PBE1PBE','scrf=(iefpcm,solvent=water) empiricaldispersion=GD3bj'],['PBEh1PBE','scrf=(iefpcm,solvent=water)'],['OHSE2PBE','scrf=(iefpcm,solvent=water)'],['mPW1PBE','scrf=(iefpcm,solvent=water)'],['mPW1PW91','scrf=(iefpcm,solvent=water)'],['APFD','scrf=(iefpcm,solvent=water)'],['TPSSh','scrf=(iefpcm,solvent=water)'],['B3P86','scrf=(iefpcm,solvent=water)'],['tpsskcis','scrf=(iefpcm,solvent=water) IOp(3/76=0870001300)'],['B3LYP','scrf=(iefpcm,solvent=water) empiricaldispersion=GD3bj'],['BHandH','scrf=(iefpcm,solvent=water)'],['BMK','scrf=(iefpcm,solvent=water) empiricaldispersion=GD3bj'],['MPWB95','scrf=(iefpcm,solvent=water) IOp(3/76=0560004400)'],['MPWPW91','scrf=(iefpcm,solvent=water) IOp(3/76=0572004280)'],['bb95','scrf=(iefpcm,solvent=water) IOp(3/76=0580004200)'],['wb97xd','scrf=(iefpcm,solvent=water)'],['wb97','scrf=(iefpcm,solvent=water)'],['wb97x','scrf=(iefpcm,solvent=water)'],['cam-b3lyp','scrf=(iefpcm,solvent=water) empiricaldispersion=GD3bj'],['LC-wHPBE','scrf=(iefpcm,solvent=water)']]

benchmarkbasis=[['6-31G(d)'],['6-31+G(d,p)','6-311+G(d,p)'],['cc-pvdz','aug-cc-pvdz']]

#CONFORMATIONAL SEARCH:
CRESTcores=16
CRESTmem=10
CRESTtime='1-00:00:00'
CRESTpartition='short,lopez'
CRESTmethod='-xnam /work/lopez/xtb/xtb_6.2.3/bin/xtb -g H2O -ewin 500 -T 14 -opt crude -subrmsd --verbose'

ORCAmethod='B3LYP/G D3BJ 6-31G(d) def2/JK RIJK NOAUTOSTART Opt cpcm(water)'
ORCAcores=10
ORCAmem=10
ORCAoptsteps=5
ORCApartition='lopez,short'
ORCAtime='1-00:00:00'


#local workflow variables
