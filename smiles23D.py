from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np
import sys


#read the smiles file
def read_input(input):
    try:
        #some smiles can use the # character - define the comment string to prevent mis-reading the input file
        allinputs=np.genfromtxt(input,dtype='str',comments="<!--")
        return(allinputs)
    except:
        print("""Could not parse smi file. Please check the format is - 

SMILES    NAME
SMILES    NAME
...     ...

""")
        exit()


#Generate 3D coordinates from smiles file
def write_coord(allinputs):
    if allinputs.ndim < 2:
        smiles = [allinputs[0]]
        names = [allinputs[1]]
    else:
        smiles=allinputs[:,0]
        names=allinputs[:,1]

    for index,smi in enumerate(smiles):
        try:
            mol = AllChem.MolFromSmiles(smi)
            mol = AllChem.AddHs(mol,addCoords=True)
            AllChem.EmbedMultipleConfs(mol,numConfs=5)
            energies=AllChem.UFFOptimizeMoleculeConfs(mol, numThreads=0)
            print("Generating UFF conformers for {0} from {1}".format(names[index],smi))
            confs=np.zeros(len(energies))
            for x,energy in enumerate(energies):
                confs[x]=energy[1]
            min=np.argmin(confs)
            AllChem.MolToPDBFile(mol,'{0}.pdb'.format(names[index]),confId=int(min))
            with open('{0}.charge'.format(names[index]),'w') as chargefile:
                chargefile.write(str(Chem.GetFormalCharge(mol)))
        except:
            print("Could not generate 3D structure for {0} with smiles {1}".format(names[index],smi))



def main():

    input=sys.argv[1]
    allinputs = read_input(input)

    #write the coordinates
    write_coord(allinputs) 

if __name__ == "__main__":
    main()


