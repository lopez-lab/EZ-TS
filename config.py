###########################
###  System Information ###
###########################
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
#OPTIMIZATIONs:
optcores=['8','16','16','16']
optmemory=['31','62','62','62']
optpartition="short,lopez"
optmethod="b3lyp"
optbasis="6-31G(d)"
#remeber force constants required for ts optimization
optroute="opt=(calcfc,ts,noeigen) freq=noraman"
opttime='1-00:00:00'
specialopts='empiricaldispersion=GD3bj scrf=(iefpcm,solvent=water)'
#BENCHMARKING
benchmarkmethods=['M11L','SVWN','SVWN5','MN12SX','M062X','M06HF','N12SX','MPWb95','PBE1PBE','PBEh1PBE','OHSE2PBE','mPW1PBE','mPW1PW91','APFD','TPSSh','B3P86','tpsskcis','B3LYP','BHandH','BMK','MPWB95','MPWPW91','bb95','wb97xd','wb97','wb97x','cam-b3lyp','LC-wHPBE']
benchmarkspecialopts=['scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water) IOp(3/76=0690003100)','scrf=(iefpcm,solvent=water) empiricaldispersion=GD3bj','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water) IOp(3/76=0870001300)','scrf=(iefpcm,solvent=water) empiricaldispersion=GD3bj','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water) empiricaldispersion=GD3bj','scrf=(iefpcm,solvent=water) IOp(3/76=0560004400)','scrf=(iefpcm,solvent=water) IOp(3/76=0572004280)','scrf=(iefpcm,solvent=water) IOp(3/76=0580004200)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water)','scrf=(iefpcm,solvent=water) empiricaldispersion=GD3bj','']
benchmarkbasis=[['6-31G(d)'],['6-31+G(d,p)','6-311+G(d,p)'],['cc-pvdz','aug-cc-pvdz','cc-pvtz','aug-cc-pvtz']]

#CONFORMATIONAL SEARCH:
CRESTcores=16
CRESTmem=62
CRESTtime='1-00:00:00'
CRESTpartition='short,lopez'
CRESTmethod=CRESTmethod='-xnam /work/lopez/xtb/xtb_6.2.3/bin/xtb -g H2O -ewin 500 -T 14 -opt crude -subrmsd --verbose'

ORCAmethod='B3LYP/G D3BJ 6-31G(d) def2/J NOAUTOSTART Opt cpcm(water)'
ORCAcores=8
ORCAmem=63
ORCApartition='lopez,short'
ORCAtime='1-00:00:00'


#local workflow variables
