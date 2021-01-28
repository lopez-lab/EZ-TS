import numpy as np
import sys
import os

workdir=os.getcwd()
infile=sys.argv[1].split('/')[-1]
infile=infile.split(".")[0]
outfile=sys.argv[2]
 ## This function read coordinates from orca out files
with open(sys.argv[1],'r') as logfile:
    log=logfile.read().splitlines()

    natom=0
    coord=[]
    xyz=[]
    atoms=[]
    for n,line in enumerate(log):
        if 'Number of atoms' in line:
            natom=int(line.split()[-1])
        if 'CARTESIAN COORDINATES (ANGSTROEM)' in line:
            coord=log[n+2:n+2+natom]
    for line in coord:
        e,x,y,z=line.split()
        x,y,z=float(x),float(y),float(z)
        atoms.append(e)
        xyz.append([x,y,z])

xyz=np.array(xyz)

with open(outfile,'w') as newxyz:
    xyzline="""{0}
converted from {1}.out\n""".format(natom, infile)
    newxyz.write(xyzline)

for i in range(0,natom):
    xyzline="""{0}    {1:.5f}    {2:.5f}    {3:.5f}\n""".format(atoms[i], xyz[i,0], xyz[i,1], xyz[i,2])
    with open(outfile,'a') as newxyz:
        newxyz.write(xyzline) 
