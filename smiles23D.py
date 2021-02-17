from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np
import sys

#Generate 3D coordinates from smiles file
input=sys.argv[1]
allinputs=np.genfromtxt(input,dtype='str')

# input should be of the format:

#NAME    SMILES
#NAME    SMILES
#...     ...

smiles=allinputs[:,0]
names=allinputs[:,1]
for b,c in enumerate(smiles):
    mol = AllChem.MolFromSmiles(c)
    mol = AllChem.AddHs(mol,addCoords=True)
    AllChem.EmbedMultipleConfs(mol,numConfs=5)
    energies=AllChem.UFFOptimizeMoleculeConfs(mol, numThreads=0)
    confs=np.zeros(len(energies))
    for x,i in enumerate(energies):
        confs[x]=i[1]
    min=np.argmin(confs)
    AllChem.MolToPDBFile(mol,'{0}.pdb'.format(names[b]),confId=int(min))
    with open('{0}.charge'.format(names[b]),'w') as chargefile:
        chargefile.write(str(Chem.GetFormalCharge(mol)))
