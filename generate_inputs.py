#new version
import sys
from config import *
import os
import numpy as np
from numpy import linalg as la
from optparse import OptionParser
import shutil

basis_dict={
    "6-31G(d)":"pople",
    "6-31+G(d,p)":"pople-plusdp",
    "6-311+G(d,p)":"pople-tz",
    "cc-pvdz":"cc-pvdz",
    "cc-pvtz":"cc-pvtz",
    "aug-cc-pvdz":"aug-cc-pvdz",
    "aug-cc-pvtz":"aug-cc-pvtz"
    }

class Element:
    ## This class is periodic table
    ## This class read atom name in various format
    ## This class return atomic properties

    def __init__(self,name):

        Periodic_Table = {
             "HYDROGEN":"1","H":"1","1":"1",
             "HELIUM":"2","He":"2","2":"2","HE":"2",
             "LITHIUM":"3","Li":"3","3":"3","LI":"3",
             "BERYLLIUM":"4","Be":"4","4":"4","BE":"4",
             "BORON":"5","B":"5","5":"5",
             "CARBON":"6","C":"6","6":"6",
             "NITROGEN":"7","N":"7","7":"7",
             "OXYGEN":"8","O":"8","8":"8",
             "FLUORINE":"9","F":"9","9":"9",
             "NEON":"10","Ne":"10","10":"10","NE":"10",
             "SODIUM":"11","Na":"11","11":"11","NA":"11",
             "MAGNESIUM":"12","Mg":"12","12":"12","MG":"12",
             "ALUMINUM":"13","Al":"13","13":"13","AL":"12",
             "SILICON":"14","Si":"14","14":"14","SI":"14",
             "PHOSPHORUS":"15","P":"15","15":"15",
             "SULFUR":"16","S":"16","16":"16",
             "CHLORINE":"17","Cl":"17","17":"17","CL":"17",
             "ARGON":"18","Ar":"18","18":"18","AG":"18",
             "POTASSIUM":"19","K":"19","19":"19",
             "CALCIUM":"20","Ca":"20","20":"20","CA":"20",
             "SCANDIUM":"21","Sc":"21","21":"21","SC":"21",
             "TITANIUM":"22","Ti":"22","22":"22","TI":"22",
             "VANADIUM":"23","V":"23","23":"23",
             "CHROMIUM":"24","Cr":"24","24":"24","CR":"24",
             "MANGANESE":"25","Mn":"25","25":"25","MN":"25",
             "IRON":"26","Fe":"26","26":"26","FE":"26",
             "COBALT":"27","Co":"27","27":"27","CO":"27",
             "NICKEL":"28","Ni":"28","28":"28","NI":"28",
             "COPPER":"29","Cu":"29","29":"29","CU":"29",
             "ZINC":"30","Zn":"30","30":"30","ZN":"30",
             "GALLIUM":"31","Ga":"31","31":"31","GA":"31",
             "GERMANIUM":"32","Ge":"32","32":"32","GE":"32",
             "ARSENIC":"33","As":"33","33":"33","AS":"33",
             "SELENIUM":"34","Se":"34","34":"34","SE":"34",
             "BROMINE":"35","Br":"35","35":"35","BR":"35",
             "KRYPTON":"36","Kr":"36","36":"36","KR":"36",
             "RUBIDIUM":"37","Rb":"37","37":"37","RB":"37",
             "STRONTIUM":"38","Sr":"38","38":"38","SR":"38",
             "YTTRIUM":"39","Y":"39","39":"39",
             "ZIRCONIUM":"40","Zr":"40","40":"40","ZR":"40",
             "NIOBIUM":"41","Nb":"41","41":"41","NB":"41",
             "MOLYBDENUM":"42","Mo":"42","42":"42","MO":"42",
             "TECHNETIUM":"43","Tc":"43","43":"43","TC":"43",
             "RUTHENIUM":"44","Ru":"44","44":"44","RU":"44",
             "RHODIUM":"45","Rh":"45","45":"45","RH":"45",
             "PALLADIUM":"46","Pd":"46","46":"46","PD":"46",
             "SILVER":"47","Ag":"47","47":"47","AG":"47",
             "CADMIUM":"48","Cd":"48","48":"48","CD":"48",
             "INDIUM":"49","In":"49","49":"49","IN":"49",
             "TIN":"50","Sn":"50","50":"50","SN":"50",
             "ANTIMONY":"51","Sb":"51","51":"51","SB":"51",
             "TELLURIUM":"52","Te":"52","52":"52","TE":"52",
             "IODINE":"53","I":"53","53":"53",
             "XENON":"54","Xe":"54","54":"54","XE":"54",
             "CESIUM":"55","Cs":"55","55":"55","CS":"55",
             "BARIUM":"56","Ba":"56","56":"56","BA":"56",
             "LANTHANUM":"57","La":"57","57":"57","LA":"57",
             "CERIUM":"58","Ce":"58","58":"58","CE":"58",
             "PRASEODYMIUM":"59","Pr":"59","59":"59","PR":"59",
             "NEODYMIUM":"60","Nd":"60","60":"60","ND":"60",
             "PROMETHIUM":"61","Pm":"61","61":"61","PM":"61",
             "SAMARIUM":"62","Sm":"62","62":"62","SM":"62",
             "EUROPIUM":"63","Eu":"63","63":"63","EU":"63",
             "GADOLINIUM":"64","Gd":"64","64":"64","GD":"64",
             "TERBIUM":"65","Tb":"65","65":"65","TB":"65",
             "DYSPROSIUM":"66","Dy":"66","66":"66","DY":"66",
             "HOLMIUM":"67","Ho":"67","67":"67","HO":"67",
             "ERBIUM":"68","Er":"68","68":"68","ER":"68",
             "THULIUM":"69","TM":"69","69":"69","TM":"69",
             "YTTERBIUM":"70","Yb":"70","70":"70","YB":"70",
             "LUTETIUM":"71","Lu":"71","71":"71","LU":"71",
             "HAFNIUM":"72","Hf":"72","72":"72","HF":"72",
             "TANTALUM":"73","Ta":"73","73":"73","TA":"73",
             "TUNGSTEN":"74","W":"74","74":"74",
             "RHENIUM":"75","Re":"75","75":"75","RE":"75",
             "OSMIUM":"76","Os":"76","76":"76","OS":"76",
             "IRIDIUM":"77","Ir":"77","77":"77","IR":"77",
             "PLATINUM":"78","Pt":"78","78":"78","PT":"78",
             "GOLD":"79","Au":"79","79":"79","AU":"79",
             "MERCURY":"80","Hg":"80","80":"80","HG":"80",
             "THALLIUM":"81","Tl":"81","81":"81","TL":"81",
             "LEAD":"82","Pb":"82","82":"82","PB":"82",
             "BISMUTH":"83","Bi":"83","83":"83","BI":"83",
             "POLONIUM":"84","Po":"84","84":"84","PO":"84",
             "ASTATINE":"85","At":"85","85":"85","AT":"85",
             "RADON":"86","Rn":"86","86":"86","RN":"86"}

        FullName=["HYDROGEN", "HELIUM", "LITHIUM", "BERYLLIUM", "BORON", "CARBON", "NITROGEN", "OXYGEN", "FLUORINE", "NEON",
              "SODIUM", "MAGNESIUM", "ALUMINUM", "SILICON", "PHOSPHORUS", "SULFUR", "CHLORINE", "ARGON", "POTASSIUM", "CALCIUM",
              "SCANDIUM", "TITANIUM", "VANADIUM", "CHROMIUM", "MANGANESE", "IRON", "COBALT", "NICKEL", "COPPER", "ZINC",
              "GALLIUM", "GERMANIUM", "ARSENIC", "SELENIUM", "BROMINE", "KRYPTON", "RUBIDIUM", "STRONTIUM", "YTTRIUM", "ZIRCONIUM",
              "NIOBIUM", "MOLYBDENUM", "TECHNETIUM", "RUTHENIUM", "RHODIUM", "PALLADIUM", "SILVER", "CADMIUM", "INDIUM", "TIN",
              "ANTIMONY", "TELLURIUM", "IODINE", "XENON", "CESIUM", "BARIUM", "LANTHANUM", "CERIUM", "PRASEODYMIUM", "NEODYMIUM",
              "PROMETHIUM", "SAMARIUM", "EUROPIUM", "GADOLINIUM", "TERBIUM", "DYSPROSIUM", "HOLMIUM", "ERBIUM", "THULIUM", "YTTERBIUM",
              "LUTETIUM", "HAFNIUM", "TANTALUM", "TUNGSTEN", "RHENIUM", "OSMIUM", "IRIDIUM", "PLATINUM", "GOLD", "MERCURY",
              "THALLIUM", "LEAD", "BISMUTH", "POLONIUM", "ASTATINE", "RADON"]

        Symbol=[ "H","He","Li","Be","B","C","N","O","F","Ne",
                "Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca",
                "Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn",
                "Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr",
                "Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn",
                "Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd",
                "Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","TM","Yb",
                "Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg",
                "Tl","Pb","Bi","Po","At","Rn"]

        Mass=[1.008,4.003,6.941,9.012,10.811,12.011,14.007,15.999,18.998,20.180,
              22.990,24.305,26.982,28.086,30.974,32.065,35.453,39.948,39.098,40.078,
              44.956,47.867,50.942,51.996,54.938,55.845,58.933,58.693,63.546,65.390,
              69.723,72.640,74.922,78.960,79.904,83.800,85.468,87.620,88.906,91.224,
              92.906,95.940,98.000,101.070,102.906,106.420,107.868,112.411,114.818,118.710,
              121.760,127.600,126.905,131.293,132.906,137.327,138.906,140.116,140.908,144.240,
              145.000,150.360,151.964,157.250,158.925,162.500,164.930,167.259,168.934,173.040,
              174.967,178.490,180.948,183.840,186.207,190.230,192.217,195.078,196.967,200.590,
              204.383,207.200,208.980,209.000,210.000,222.000]

        # Van der Waals Radius, missing data replaced by 2.00
        Radii=[1.20,1.40,1.82,1.53,1.92,1.70,1.55,1.52,1.47,1.54,
               2.27,1.73,1.84,2.10,1.80,1.80,1.75,1.88,2.75,2.31,
               2.11,2.00,2.00,2.00,2.00,2.00,2.00,1.63,1.40,1.39,
               1.87,2.11,1.85,1.90,1.85,2.02,3.03,2.49,2.00,2.00,
               2.00,2.00,2.00,2.00,2.00,1.63,1.72,1.58,1.93,2.17,
               2.00,2.06,1.98,2.16,3.43,2.68,2.00,2.00,2.00,2.00,
               2.00,2.00,2.00,2.00,2.00,2.00,2.00,2.00,2.00,2.00,
               2.00,2.00,2.00,2.00,2.00,2.00,2.00,1.75,1.66,1.55,
               1.96,2.02,2.07,1.97,2.02,2.20]

        # Covalent Radii, missing data replaced by 1.50
        CovRad=[ 0.38,  0.32,  1.34,  0.9 ,  0.82,  0.77,  0.75,  0.73,  0.71,
                 0.69,  1.54,  1.3 ,  1.18,  1.11,  1.06,  1.02,  0.99,  0.97,
                 1.96,  1.74,  1.44,  1.36,  1.25,  1.27,  1.39,  1.25,  1.26,
                 1.21,  1.38,  1.31,  1.26,  1.22,  1.19,  1.16,  1.14,  1.1 ,
                 2.11,  1.92,  1.62,  1.48,  1.37,  1.45,  1.56,  1.26,  1.35,
                 1.31,  1.53,  1.48,  1.44,  1.41,  1.38,  1.35,  1.33,  1.3,
                 2.25,  1.98,  1.69,  1.5 ,  0.11,  1.5 ,  1.5 ,  1.5 ,  1.5 ,
                 1.5 ,  1.5 ,  1.5 ,  1.5 ,  1.5 ,  1.5 ,  1.5 ,  1.5 ,  1.6 ,
                 1.5 ,  1.38,  1.46,  1.59,  1.28,  1.37,  1.28,  1.44,  1.49,
                 1.48,  1.47,  1.46,  1.5 ,  1.5 ,  1.45]

        self.__name = int(Periodic_Table[name])
        self.__FullName = FullName[self.__name-1]
        self.__Symbol = Symbol[self.__name-1]
        self.__Mass = Mass[self.__name-1]
        self.__Radii = Radii[self.__name-1]
        self.__CovR  = CovRad[self.__name-1]

    def getFullName(self):
        return self.__FullName
    def getSymbol(self):
        return self.__Symbol
    def getUpperSymbol(self):
        return self.__Symbol.upper()
    def getMass(self):
        return self.__Mass
    def getNuc(self):
        return self.__name
    def getNelectron(self):
        return self.__name
    def getRadii(self):
        return self.__Radii
    def getCovR(self):
        return self.__CovR

#################################################################################################################################################

#################
### Functions ###
#################

def Ang(xyz,a,b,c):
    #a<-b->c
    a=xyz[a]
    b=xyz[b]
    c=xyz[c]
    v1=a-b
    v2=c-b
    v1=v1/la.norm(v1)
    v2=v2/la.norm(v2)
    cosa=np.dot(v1,v2)
    alpha=np.arccos(cosa)*57.2958
    return alpha

def Deh(xyz,a,b,c,d):
    #  n1       n2
    #   |       |
    #a<-b->c b<-c->d
    a=xyz[a]
    b=xyz[b]
    c=xyz[c]
    d=xyz[d]
    v1=a-b
    v2=c-b
    v3=b-c
    v4=d-c
    n1=np.cross(v1,v2)
    n2=np.cross(v3,v4)
    n1=n1/la.norm(n1)
    n2=n2/la.norm(n2)
    cosb=np.dot(n1,n2)
    beta=np.arccos(cosb)*57.2958
    return beta

def ReadXYZ(title):
## This function read coordinates from .xyz
    with open('%s.xyz' % (title),'r') as xyzfile:
        coord=xyzfile.read().splitlines()
        natom=int(coord[0])
        #Try to get charge information from title line
        if 'charge=' in coord[1].lower():
            try:
                charge = int(coord[1].split('=')[-1])
            except:
                print('Could not read charge for {0}, be sure charge=interger'.format(title))
                exit()
        else:
            charge=0
        multiplicity=1

        coord=coord[2:2+natom]

    xyz=[]
    atoms=[]

    for i in coord:
        e,x,y,z=i.split()
        n=Element(e).getNuc()
        x,y,z=float(x),float(y),float(z)
        atoms.append(n)
        xyz.append([x,y,z])
    
    xyz=np.array(xyz)
    return charge,multiplicity,atoms,xyz


def ReadG16(title):
    ''' Read a log file '''

    with open('{0}.log'.format(title),'r') as logfile:
        log=logfile.read().splitlines()

    natom=0
    coord=[]
    xyz=[]
    atoms=[]
    for n,line in enumerate(log):
        if 'NAtoms' in line:
            natom=int(line.split()[1])
        if 'Standard orientation' in line:
            coord=log[n+5:n+5+natom]
        if 'Multiplicity =' in line:
            charge=line.split()[2]
            multiplicity=line.split()[5]
    for line in coord:
        c,e,t,x,y,z=line.split()
        n=Element(e).getNuc()
        x,y,z=float(x),float(y),float(z)
        atoms.append(n)
        xyz.append([x,y,z])

    xyz=np.array(xyz)
    return charge,multiplicity,atoms,xyz

def FindAx(D,atoms,axis):
    '''find axis atoms given the atomic number'''

    pairs=[]
    dists=[]

    for n,x in enumerate(atoms):
        for m,y in enumerate(atoms):
            if x == axis and y == axis and n != m:
                pairs.append([n,m])
                dists.append(D[n,m])
    axis1,axis2=pairs[np.argmin(dists)]
    return axis1,axis2

def FindCnct(D,frag,axis):
    '''find connect atom given the atom index expect for the other one'''

    cnct=np.argmin([D[axis,x] for x in frag])
    cnct=frag[cnct]

    return cnct

def Findedges(adjacent,C):
    '''walk along the edge of connected graph'''
    global frag1
#    new=0
    for n,i in enumerate(adjacent):
#        print(n,i,frag1)
        if i == 1 and n not in frag1:
#            new+=1
            frag1.append(n)
            Findedges(C[n,:],C)
#    if new == 0:
#        print(frag1)

def Frag(atoms,xyz,ax):
    '''do fragmentation and return coordinates map
    axis format [C1,A1,A2,C2]
    only when axis[2] == -1, non-integer in axis[1] is accepted '''

    natom=len(atoms)
    D=np.diag([99. for x in atoms]) # distance matrix
    C=np.diag(atoms) # connectivity matrix
    for n,x in enumerate(xyz):
        for m,y in enumerate(xyz[n+1:]):
            r=la.norm(x-y)
            D[n,m+n+1]=r
            D[m+n+1,n]=r
            r1=Element(str(int(atoms[n]))).getCovR()
            r2=Element(str(int(atoms[m+n+1]))).getCovR()
            if 0.1 < r < (r1+r2)*1.3:
                C[n,m+n+1]=1
                C[m+n+1,n]=1

    if ax[2] == -1:   # find two same elements with shortest distance and then search two connected atoms
        a1,a2=FindAx(D,atoms,Element(ax[1]).getNuc())
        c1=-1
        c2=-1
    else:
        c1,a1,a2,c2=ax
        c1,a1,a2,c2=int(c1)-1,int(a1)-1,int(a2)-1,int(c2)-1

    # cut the axis bond
    C[a1,a2]=0
    C[a2,a1]=0

    # update global fragment 1
    Findedges(C[a1,:],C)
    frag2=[x for x in range(natom) if x not in frag1]

    if c1 < 0:
        c1=FindCnct(D,frag1,a1)

    if c2 < 0:
        c2=FindCnct(D,frag2,a2)

    d1=FindCnct(D,[x for x in frag1 if x != a1],c1)
    d2=FindCnct(D,[x for x in frag2 if x != a2],c2)
    return d1,c1,a1,a2,c2,d2,frag1,frag2

def rotate(xyz,v1,v2,frag,angle):
    '''This function rotate molecule around atom1 atom2'''

    output=[]
    k=v1-v2
    k=k/la.norm(k)
    for n,v in enumerate(xyz-v2):
        if n in frag:
            vcosa=v*np.cos(angle/180.*np.pi)
            kxvsina=np.cross(k,v)*np.sin(angle/180.*np.pi)
            kkv1_cosa=k*(np.dot(k,v))*(1-np.cos(angle/180.*np.pi))
            #print (vcosa,kxvsina,kkv1_cosa)
            vrot=vcosa+kxvsina+kkv1_cosa
            output.append(vrot)
        else:
            output.append(v)

    output=np.array(output)
    output+=v2
    return output

def Printfrag(frag):

    info=''
    for n,i in enumerate(sorted(frag)):
        info+='%5s' % (i)
        if (n+1) % 10 == 0 or n == len(frag):
            info+='\n'

    return info

def MoRot(file,ax,ang,index,optcores,optmemory,optmethod,optbasis,optroute,ts_guess_dir,specialopts):
    '''This function rotate dihedral for a given molecule, axis, and angles.'''

    ## read coordinates
    filename=file.split('/')[-1]
    #print(filename)
    title,ext=filename.split('.')
    
    if ext == 'xyz':
        charge,multiplicity,atoms,xyz=ReadXYZ(title)
    elif ext == 'log':
        charge,multiplicity,atoms,xyz=ReadG16(title)
    else:
        print('\n!!! Unkown coordinate file format !!!\n')
        exit()

    ## find connectivity
    d1,c1,a1,a2,c2,d2,frag1,frag2=Frag(atoms,xyz,ax) # all strings are converted to integers

    ## perform rotation

    origin_rot=[Deh(xyz,d1,c1,a1,a2),
                Deh(xyz,d2,c2,a2,a1),
                Deh(xyz,c1,a1,a2,c2),
                Ang(xyz,c1,a1,a2),
                Ang(xyz,c2,a2,a1)]

    target_rot=origin_rot.copy()
    shift_rot=[0,0,0,0,0]

    if ang[0] != None:
        a=float(ang[0])
        v1=xyz[a1]
        v2=xyz[c1]
        rot=origin_rot[0]-a
        target_rot[0]=a
        shift_rot[0]=rot
        xyz1=rotate(xyz,v1,v2,frag1,rot)
        ang1=Deh(xyz1,d1,c1,a1,a2)
        xyz2=rotate(xyz,v1,v2,frag1,-rot)
        ang2=Deh(xyz2,d1,c1,a1,a2)

        if np.abs(np.abs(ang1)-np.abs(a)) < np.abs(np.abs(ang2)-np.abs(a)):
            xyz=xyz1
        else:
            xyz=xyz2

    if ang[1] != None:
        a=float(ang[1])
        v1=xyz[a2]
        v2=xyz[c2]
        rot=origin_rot[1]-a
        target_rot[1]=a
        shift_rot[1]=rot
        xyz1=rotate(xyz,v1,v2,frag2,rot)
        ang1=Deh(xyz1,d2,c2,a2,a1)
        xyz2=rotate(xyz,v1,v2,frag2,-rot)
        ang2=Deh(xyz2,d2,c2,a2,a1)

        if np.abs(np.abs(ang1)-np.abs(a)) < np.abs(np.abs(ang2)-np.abs(a)):
            xyz=xyz1
        else:
            xyz=xyz2

    if ang[2] != None:
        a=float(ang[2])
        v1=xyz[a2]
        v2=xyz[a1]
        rot=origin_rot[2]-a
        target_rot[2]=a
        shift_rot[2]=rot
        xyz1=rotate(xyz,v1,v2,frag1,rot)
        ang1=Deh(xyz1,c1,a1,a2,c2)
        xyz2=rotate(xyz,v1,v2,frag1,-rot)
        ang2=Deh(xyz2,c1,a1,a2,c2)

        if np.abs(np.abs(ang1)-np.abs(a)) < np.abs(np.abs(ang2)-np.abs(a)):
            xyz=xyz1
        else:
            xyz=xyz2

    if ang[3] != None:
        a=float(ang[3])
        v1=xyz[c1]-xyz[a1]
        v2=xyz[a2]-xyz[a1]
        n1=np.cross(v1,v2)
        n1=n1/la.norm(n1)
        v1=n1+xyz[a1]
        v2=xyz[a1]
        rot=origin_rot[3]-a
        target_rot[3]=a
        shift_rot[3]=rot
        xyz1=rotate(xyz,v1,v2,frag1,rot)
        ang1=Ang(xyz1,c1,a1,a2)
        xyz2=rotate(xyz,v1,v2,frag1,-rot)
        ang2=Ang(xyz2,c1,a1,a2)

        if np.abs(np.abs(ang1)-np.abs(a)) < np.abs(np.abs(ang2)-np.abs(a)):
            xyz=xyz1
        else:
            xyz=xyz2

    if ang[4] != None:
        a=float(ang[4])
        v1=xyz[c2]-xyz[a2]
        v2=xyz[a1]-xyz[a2]
        n1=np.cross(v1,v2)
        n1=n1/la.norm(n1)
        v1=n1+xyz[a2]
        v2=xyz[a2]
        rot=origin_rot[4]-a
        target_rot[4]=a
        shift_rot[4]=rot
        xyz1=rotate(xyz,v1,v2,frag2,rot)
        ang1=Ang(xyz1,c2,a2,a1)
        xyz2=rotate(xyz,v1,v2,frag2,-rot)
        ang2=Ang(xyz2,c2,a2,a1)

        if np.abs(np.abs(ang1)-np.abs(a)) < np.abs(np.abs(ang2)-np.abs(a)):
            xyz=xyz1
        else:
            xyz=xyz2

    # use coordinates to write ts_guess input file
    coord=''
    for n,line in enumerate(xyz):
        x,y,z=line
        e=Element(str(int(atoms[n]))).getSymbol()
        coord+='%-5s%16.8f%16.8f%16.8f\n' % (e,x,y,z)

    com_name = '{0}/{1}-rot-{2}.com'.format(ts_guess_dir,title,index)
    chk_name = '{0}-rot-{1}.chk'.format(title,index)
    out_coord=write_com(com_name,chk_name,optcores[0],optmemory[0],optmethod,optbasis,ts_guessroute,specialopts,charge,multiplicity)
    #add the coordinates 
    with open(com_name,'a') as out:
        out.write(coord)
        out.write(' ')

    #print out rotation information
    info_frag1=Printfrag(frag1)
    info_frag2=Printfrag(frag2)
    info="""
  Tilte: %s-%s
-------------------------------------------------------
  D2:    %4s
  C1:    %4s
  A1:    %4s
  A2:    %4s
  C2:    %4s
  D2:    %4s
  R1:    %5d - %5d = %5d
  R2:    %5d - %5d = %5d
  R12:   %5d - %5d = %5d
  V1:    %5d - %5d = %5d
  V2:    %5d - %5d = %5d
  Natom: %4s
  Frag1: %4s
%s
  Frag2: %4s
%s
-------------------------------------------------------
""".format(title,index,d1+1,c1+1,a1+1,a2+1,c2+1,d2+1,origin_rot[0],target_rot[0],shift_rot[0],origin_rot[1],target_rot[1],shift_rot[1],origin_rot[2],target_rot[2],shift_rot[2],origin_rot[3],target_rot[3],shift_rot[3],origin_rot[4],target_rot[4],shift_rot[4],len(xyz),len(frag1),info_frag1,len(frag2),info_frag2)

    with open('rotation.out','a') as log:
        log.write(info)

    natom=len(xyz)
    return charge,multiplicity,c1,a1,a2,c2,title,xyz,out_coord,natom


def ReadOpt(axis,angles):
    '''This function read axis and angles from the given options'''

    opt_axis=[-1,-1,-1,-1]
    for n,i in enumerate(axis):
        if   i == 'C1':
            opt_axis[0]=axis[n+1]
        elif i == 'A1':
            opt_axis[1]=axis[n+1]
        elif i == 'A2':
            opt_axis[2]=axis[n+1]
        elif i == 'C2':
            opt_axis[3]=axis[n+1]

    opt_angles=[None,None,None,None,None]
    for n,i in enumerate(angles):
        if   i == 'R1':
            opt_angles[0]=angles[n+1]
        elif i == 'R2':
            opt_angles[1]=angles[n+1]
        elif i == 'R12':
            opt_angles[2]=angles[n+1]
        elif i == 'V1':
            opt_angles[3]=angles[n+1]
        elif i == 'V2':
            opt_angles[4]=angles[n+1]

    return opt_axis, opt_angles

def Readlist(list,opt_axis,opt_angles):
    '''This function read coordinates file, axis, and angles from input list.'''
    jobs=[]
    name_list=[]
    with open(list,'r') as inp:
        files=inp.read().splitlines()

    for i in files:
        out_axis=opt_axis.copy()
        out_angles=opt_angles.copy()
        file=i.split()[0]
        title=file.split('/')[-1].split('.')[0]
        name_list.append(title)
        name_index=0
        for j in name_list:
            if j == title:
                name_index+=1
        opt=[x.upper() for x in i.split()[1:]]
        inp_axis,inp_angles=ReadOpt(opt,opt)

        for n,j in enumerate(inp_axis):
            if j != out_axis[n] and j != -1:
                out_axis[n] = j
        for n,j in enumerate(inp_angles):
            if j != out_angles[n] and j != None:
                out_angles[n] = j

        jobs.append([file,out_axis,out_angles,name_index])

    return jobs


#################################################################################################################################################

#################################################
### Functions to write input/submission files ###
#################################################


def write_com(com_name,chk_name,cores,memory,method,basis,route,specialopts,charge,multiplicity):
    '''General Gaussian input template'''

    com="""%chk={0}
%nprocs={1}
%mem={2}GB
# {3}/{4} {5} {6}

auto-ts generator

{7} {8}
""".format(chk_name,cores,memory,method,basis,route,specialopts,charge,multiplicity)
    with open(com_name,'w') as out:
        out.write(com)

def write_benchmarking_com(com_name,chk_name,cores,memory,method,basis,route,specialopts,charge,multiplicity,tier,basislist,title,previous_dir,suffix):
    '''General Gaussian input template for benchmarking'''

    route = route.replace('freq=noraman','')
    if previous_dir == 'lowest_ts':
        optroute='opt=(readfc,ts,noeigen)'

        if tier > 0:
            oldchk='{0}-{1}-{2}'.format(title,method,basis_dict[basislist[tier-1]])

            com="""%oldchk={9}-tier{10}.chk
%chk={0}
%nprocs={1}
%mem={2}GB
# {3}/{4} {5} {6} geom=check guess=read

auto-ts generator

{7} {8}

--Link1--
%chk={0}
%nprocs={1}
%mem={2}GB
# {3}/{4} {6} geom=check guess=read freq=noraman

freq

{7} {8}

""".format(chk_name,cores,memory,method,basis,optroute,specialopts,charge,multiplicity,oldchk,tier-1)

        else:
            com="""%oldchk=../{10}/{9}.chk
%chk={0}
%nprocs={1}
%mem={2}GB
# {3}/{4} {5} {6} geom=check

auto-ts generator

{7} {8}

--Link1--
%chk={0}
%nprocs={1}
%mem={2}GB
# {3}/{4} {6} geom=check guess=read freq=noraman

freq

{7} {8}

""".format(chk_name,cores,memory,method,basis,route,specialopts,charge,multiplicity,title,previous_dir)

    elif previous_dir == 'irc':
        optroute='opt'
        oldchk='{0}-{1}-{2}'.format(title,method,basis_dict[basis])

        com="""%oldchk=../{10}/{9}-tier{11}-{12}.chk
%chk={0}
%nprocs={1}
%mem={2}GB
# {3}/{4} {5} {6} geom=check

auto-ts generator

{7} {8}

--Link1--
%chk={0}
%nprocs={1}
%mem={2}GB
# {3}/{4} {6} geom=check guess=read freq=noraman

freq

{7} {8}

""".format(chk_name,cores,memory,method,basis,route,specialopts,charge,multiplicity,oldchk,previous_dir,tier,suffix)


    with open(com_name,'w') as out:
        out.write(com)



################
### ts_guess ###
################
class ts_guess():

    def _sbatch(tmptitle,optpartition,optcores,optmemory,opttime,jobs_per_mol,ts_guess_dir,title,runlog,g16root):
        '''submission script for ts_guess optimizations, which sets up failed script and conf_search dependecy jobs'''

        sbatch="""#!/bin/bash
#SBATCH --job-name={0}-tsguess
#SBATCH --output={6}/out.o
#SBATCH --error={6}/out.e
#SBATCH --partition={1}
#SBATCH --nodes=1
#SBATCH --ntasks={2}
#SBATCH --mail-type=END
#SBATCH --mem={3}G
#SBATCH --time={4}
#SBATCH --array=1-{5}
hostname

work={6}
cd $work

if [[ $SLURM_ARRAY_TASK_ID == 1 ]]
    then
    sbatch --dependency=afterok:$SLURM_ARRAY_JOB_ID ../conf_search/{7}/CREST/{7}-CREST.sbatch
    sbatch --dependency=afternotok:$SLURM_ARRAY_JOB_ID {7}-failed.sbatch
    time=$(date)
    echo "$SLURM_JOB_NAME $time" >> ../status.txt
    echo "$SLURM_JOB_NAME autots started in $work" >> {8}/{7}
else
    sleep 120s
fi

input=$(sed "${{SLURM_ARRAY_TASK_ID}}q;d" {7}-coms.txt)
export INPUT=$input
export WORKDIR=$work
export GAUSS_SCRDIR=$work
export g16root={9}
. $g16root/g16/bsd/g16.profile

cd $WORKDIR
$g16root/g16/g16 $INPUT

#if it's not the freq only step
optstep=$(grep "opt=" $INPUT -c )
if [[ $optstep -gt 0 ]]
    then
    #at least 1 station for this guess optimization - otherwise fail
    station=$(grep "Station" -c ${{INPUT%.*}}.log)
    if [[ $station -lt 1 ]]
       then
       exit 1234
    fi
    freq=$(tac ${{INPUT%.*}}.log | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
    if [[ $freq -gt 1 ]]
        then 
        exit 1234
    fi

else 
    #if it is the freq step, check that an energy is present - otherwise fail
    energy=$(grep "Sum of electronic and thermal Free Energies" -c ${{INPUT%.*}}.log)
    if [[ $energy -lt 1 ]]
        then
            echo "ts_guess/${{INPUT%.*}}.log did not complete frequencies after 2 tries optimizing - check structure" >> ../status.txt
            exit 1234
    fi
fi

""".format(tmptitle,optpartition,optcores,optmemory,opttime,jobs_per_mol,ts_guess_dir,title,runlog,g16root)
        with open('{0}/{1}-submit.sbatch'.format(ts_guess_dir,title),'w') as batch:
            batch.write(sbatch)


    def _failed(tmptitle,short_partition,ts_guess_dir,title,charge,multiplicity,conf_search_dir,ts_guessroute):
        '''handles Gaussian failures in ts_guess optimization - tries resubmitting twice, then just does a frequency calculation'''

        failed="""#!/bin/bash
#SBATCH --job-name={0}-ts_guess-failed
#SBATCH --output={2}/resubmit.o
#SBATCH --error={2}/resubmit.e
#SBATCH --partition={1}
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --time=00:20:00
hostname

work={2}
cd $work
touch failed-script-ran
time=$(date)
echo "$SLURM_JOB_NAME $time" >> ../status.txt

if test -f {3}-resubmit.txt
    then
    nresub=$(sed "1q;d" {3}-resubmit.txt)
else
    nresub=0
fi
nresub=$((nresub+=1))
if [[ $nresub -lt 2 ]]
    then
    rm {3}-resubmit.txt
    echo $nresub >> {3}-resubmit.txt
    for i in {3}-rot*log
        do
        finished=$( grep 'Station' -c $i )
        freq=$(tac $i | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )

        if [[ $finished -lt 1 ]]
            then
            sed -i '1,/{4} {5}/!d' ${{i%.*}}.com
            obabel $i -o xyz |tail -n +3 >> ${{i%.*}}.com
            echo " " >> ${{i%.*}}.com
            echo ${{i%.*}}.com >> {3}-resubmit.txt

        elif [[ $freq -gt 1 ]]
            then
            sed -i '1,/{4} {5}/!d' ${{i%.*}}.com
            obabel $i -o xyz |tail -n +3 >> ${{i%.*}}.com
            echo " " >> ${{i%.*}}.com
            echo ${{i%.*}}.com >> {3}-resubmit.txt
                
        else
            energy=$(grep "Sum of electronic and thermal Free Energies" -c $i)
            if [[ $energy -lt 1 ]]
                then
                sed -i '1,/{4} {5}/!d' ${{i%.*}}.com
                obabel $i -o xyz |tail -n +3 >> ${{i%.*}}.com
                echo " " >> ${{i%.*}}.com
                echo ${{i%.*}}.com >> {3}-resubmit.txt
            fi
        fi

    done
    toresub=$(cat {3}-resubmit.txt |wc -l)
    sed -i "s/#SBATCH --array=.*/#SBATCH --array=2-$toresub/g" {3}-submit.sbatch
    sed -i "s/{3}-coms.txt/{3}-resubmit.txt/g" {3}-submit.sbatch
    ID=$(sbatch --parsable {3}-submit.sbatch)
    sbatch --dependency=afterok:$ID {6}/{3}/CREST/{3}-CREST.sbatch
    sbatch --dependency=afternotok:$ID {3}-failed.sbatch

elif [[ $nresub == 2 ]]
    then
    touch freqonly
    rm {3}-resubmit.txt
    echo $nresub >> {3}-resubmit.txt
    for i in {3}-rot*log
        do
        finished=$( grep 'Station' -c $i )
        freq=$(tac $i | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
       
        if [[ $finished -lt 1 ]]
            then
            sed -i '1,/{4} {5}/!d' ${{i%.*}}.com
            obabel $i -o xyz |tail -n +3 >> ${{i%.*}}.com
            echo " " >> ${{i%.*}}.com
            echo ${{i%.*}}.com >> {3}-resubmit.txt
            sed -i 's/{7}/freq=noraman/g' ${{i%.*}}.com
            
        elif [[ $freq -gt 1 ]]
            then
            sed -i '1,/{4} {5}/!d' ${{i%.*}}.com
            obabel $i -o xyz |tail -n +3 >> ${{i%.*}}.com
            echo " " >> ${{i%.*}}.com
            echo ${{i%.*}}.com >> {3}-resubmit.txt
            sed -i 's/{7}/freq=noraman/g' ${{i%.*}}.com
                
        else
            energy=$(grep "Sum of electronic and thermal Free Energies" -c $i)
            if [[ $energy -lt 1 ]]
                then
                sed -i '1,/{4} {5}/!d' ${{i%.*}}.com
                obabel $i -o xyz |tail -n +3 >> ${{i%.*}}.com
                echo " " >> ${{i%.*}}.com
                echo ${{i%.*}}.com >> {3}-resubmit.txt
                sed -i 's/{7}/freq=noraman/g' ${{i%.*}}.com
            fi
        fi
    done
    toresub=$(cat {3}-resubmit.txt |wc -l)
    sed -i "s/#SBATCH --array=.*/#SBATCH --array=2-$toresub/g" {3}-submit.sbatch
    sed -i "s/{3}-coms.txt/{3}-resubmit.txt/g" {3}-submit.sbatch
    ID=$(sbatch --parsable {3}-submit.sbatch)
    sbatch --dependency=afterok:$ID {6}/{3}/CREST/{3}-CREST.sbatch
    sbatch --dependency=afternotok:$ID {3}-failed.sbatch
fi
""".format(tmptitle,short_partition,ts_guess_dir,title,charge,multiplicity,conf_search_dir,ts_guessroute)
        with open('{0}/{1}-failed.sbatch'.format(ts_guess_dir,title), 'w') as batch:
            batch.write(failed)


###################
### conf_search ###
###################
class conf_search():

    def _CREST_constraints(c1,c2,a1,a2,tmptitle,CRESTdir,title,natom):
        '''Write the CREST constriants file'''

        #CREST index starts at 1
        C1=c1+1
        C2=c2+1
        A1=a1+1
        A2=a2+1
        missing=[]
        numbers=[C1, A1, A2, C2]
        numbers.sort()
        numbers.insert(0, 0)  # add the minimum value on begining of the list
        numbers.append(natom + 1)  # add the maximum value at the end of the list
        for rank in range(0, len(numbers) - 1):
            if numbers[rank + 1] - numbers[rank] > 2:
                missing.append("%s-%s" % (numbers[rank] + 1, numbers[rank + 1] - 1))
            elif numbers[rank + 1] - numbers[rank] == 2:
                missing.append(str(numbers[rank] + 1))
        missing = str(missing)[1:-1]
        include = missing.replace("'", "")
    
        constraints = """$constrain
angle: {0}, {1}, {2}, auto
angle: {3}, {4}, {5}, auto
dihedral: {0}, {1}, {2}, {3}, auto
force constant=1.0
reference={6}.ref
$metadyn
atoms: {7}
$end""".format(C1, A1, A2, C2, A2, A1, tmptitle, include)
        with open('{0}/{1}.c'.format(CRESTdir, title), 'w') as constrain:
            constrain.write(constraints)


    def _CREST_sbatch(tmptitle,CRESTpartition,CRESTcores,CRESTmem,CRESTtime,ts_guess_dir,title,utilities_dir,XTBPATH,LD_LIBRARY_PATH,CRESTdir,CRESTmethod,c1,a1,a2,c2):
        '''Write the CREST submission script'''

        sbatch = """#!/bin/bash
#SBATCH --job-name={0}-CREST
#SBATCH --output={10}/out.o
#SBATCH --error={10}/out.e
#SBATCH --partition={1}
#SBATCH --nodes=1
#SBATCH --ntasks={2}
#SBATCH --mem={3}G
#SBATCH --time={4}
hostname

cd {5}
time=$(date)
echo "$SLURM_JOB_NAME $time" >> ../status.txt
if test -f {6}-ts-energies.txt
    then
    rm {6}-ts-energies.txt
fi

#old bash get_lowest script
#bash {7}/get-lowest.sh {6} ts_guess

#new python get_lowest script (also calculates dihedrals to filter more bad TS structures)
python3 ../utilities/get_lowest.py {6} {12} {13} {14} {15} ts_guess

ulimit -s unlimited
export OMP_STACKSIZE={3}G
export OMP_NUM_THREADS={2},1

export XTBPATH={8}
export XTBHOME=$XTBPATH
export OMP_MAX_ACTIVE_LEVELS=1
export LD_LIBRARY_PATH=${{LD_LIBRARY_PATH}}:${{XTBHOME}}/lib
export PYTHONPATH=${{PYTHONPATH}}:${{XTBHOME}}/python
export LD_LIBRARY_PATH={9}

work={10}
cd $work
#reset next step to make resubmission easier
sed -i "0,/#SBATCH --array=.*/s//#SBATCH --array=1-END%100/g" ../ORCA/{6}-ORCA.sbatch

cp {6}.xyz {0}.xyz
cp {6}.c {0}.c
cp {6}.xyz {0}.ref

$XTBPATH/crest {0}.xyz {11} -cinp {0}.c > {6}.out
cp crest_conformers.xyz ../ORCA/{6}-all.xyz

#ensure that CREST did not capitalize halogens
sed -i 's/CL/Cl/g' ../ORCA/{6}-all.xyz
sed -i 's/BR/Br/g' ../ORCA/{6}-all.xyz

obabel ../ORCA/{6}-all.xyz -O ../ORCA/{6}-all-sorted-conf.xyz -m
sleep 120s
nstruct=$(ls -la ../ORCA/{6}-all-sorted-conf*.xyz |wc -l)
sed -i "s/END/$nstruct/g" ../ORCA/{6}-ORCA.sbatch
ORCAID=$(sbatch --parsable ../ORCA/{6}-ORCA.sbatch)
    """.format(tmptitle,CRESTpartition,CRESTcores,CRESTmem,CRESTtime,ts_guess_dir,title,utilities_dir,XTBPATH,LD_LIBRARY_PATH,CRESTdir,CRESTmethod,c1,a1,a2,c2)
        with open('{0}/{1}-CREST.sbatch'.format(CRESTdir,title),'w') as batch:
            batch.write(sbatch)


    def _ORCA_input(ORCAmethod,ORCAcores,ORCAmem,title,c1,c2,a1,a2,ORCAdir,ORCAoptsteps,charge,multiplicity):
        '''Write ORCA input file with constraints'''

        actualmem = int(ORCAmem / ORCAcores)
        #ORCA atom indecies start at 0
        inputfile = """!{0}
%pal nprocs {1} end
%Maxcore {2}000
%geom
MaxIter {3}
Constraints
{{C {5} C}}
{{C {6} C}}
{{C {7} C}}
{{C {8} C}}
end
end
*xyzfile {9} {10} FILE
    """.format(ORCAmethod, ORCAcores, actualmem, ORCAoptsteps,title,c1,a1,a2,c2,charge,multiplicity)
        with open('{0}/{1}.inp'.format(ORCAdir,title), 'w') as ORCAinput:
            ORCAinput.write(inputfile)


    def _ORCA_sbatch(tmptitle,ORCAcores,ORCAtime,ORCApartition,ORCAmem,ORCAdir,ORCA_EXE,OPENMPI,title,ORCAmethod,errorlog):
        '''Write ORCA sbatch'''

        sbatch = """#!/bin/sh
## script for ORCA-4.2.1
#SBATCH --job-name={0}-ORCA
#SBATCH --nodes=1
#SBATCH --ntasks={1}
#SBATCH --time={2}
#SBATCH --partition={3}
#SBATCH --mem={4}Gb
#SBATCH --output={5}/out.o
#SBATCH --error={5}/out.e
#SBATCH --array=1-END%100

export WORKDIR={5}
export ORCA_EXE={6}
export OPENMPI={7}
export LD_LIBRARY_PATH=$OPENMPI/lib:$ORCA_EXE:$LD_LIBRARY_PATH
export PATH=$OPENMPI/bin:$PATH

cd $WORKDIR
if [[ $SLURM_ARRAY_TASK_ID == 1 ]]
    then
    rm {8}*conf*.out
    nstruct=$(ls -la {8}-all-sorted-conf*.xyz |wc -l)
    inp=$(cat {8}.inp)
    for ((i=1;i<=nstruct;i++))
        do
        echo -e "${{inp/FILE/{8}-all-sorted-conf$i.xyz}}" > {8}-conf$i.inp
    done

    #reset next steps for easier resubmission
    sed -i "0,/#SBATCH --array=.*/s//#SBATCH --array=1-10/g" ../../../conf_opt/{8}-submit.sbatch
    sed -i 's/{8}-NEEDS_MANUAL_FIX.txt/{8}-coms.txt/g' ../../../conf_opt/{8}-submit.sbatch
    sed -i 's/{8}-resubmit.txt/{8}-coms.txt/g' ../../../conf_opt/{8}-submit.sbatch
    rm ../../../conf_opt/{8}-conf*log
    
    if test -f ../../../conf_opt/{8}-resubmit.txt
        then
        rm ../../../conf_opt/{8}-resubmit.txt
    fi
    if test -f ../../../conf_opt/{8}-NEEDS_MANUAL_FIX.txt
        then
        rm ../../../conf_opt/{8}-NEEDS_MANUAL_FIX.txt
    fi
    
    sbatch --dependency=afterany:$SLURM_ARRAY_JOB_ID ../../../conf_opt/{8}-submit.sbatch
    time=$(date)
    echo "$SLURM_JOB_NAME $time" >> ../../../status.txt
else
    sleep 120s
fi

INPUT={8}-conf${{SLURM_ARRAY_TASK_ID}}

$ORCA_EXE/orca $INPUT.inp > $INPUT.out
date >> $INPUT.out

converged=$(grep "SCF NOT CONVERGED AFTER" -c $INPUT.out)
unreliablestep=$(grep "HUGE, UNRELIABLE STEP WAS ABOUT TO BE TAKEN" -c $INPUT.out)
if [[ $unreliablestep -gt 0 ]] || [[ $converged -gt 0 ]]
    then
        sed -i 's#{9}#{9} Slowconv NOSOSCF DIIS#g' $INPUT.inp
        $ORCA_EXE/orca $INPUT.inp > $INPUT.out
        date >> $INPUT.out
        converged=$(grep "SCF NOT CONVERGED AFTER" -c $INPUT.out)
        if [[ $converged -gt 0 ]]
            then
            energies=$(grep "FINAL SINGLE POINT ENERGY" -c $INPUT.out)
            if [[ $energies -gt 0 ]]
                then
                echo "$INPUT did not converge last scf, but previous energy was taken" >> {10}/{8}
        exit 0
            else
                echo "FINAL SINGLE POINT ENERGY     500" >> $INPUT.out
                exit 0
fi
fi
fi

    """.format(tmptitle,ORCAcores,ORCAtime,ORCApartition,ORCAmem,ORCAdir,ORCA_EXE,OPENMPI,title,ORCAmethod,errorlog)
        with open('{0}/{1}-ORCA.sbatch'.format(ORCAdir,title), 'w') as batch:
            batch.write(sbatch)


##################################
# Conformer Optimization Scripts #
##################################

class conf_opt():

    def _inputs(conf_opt_dir,title,optcores,optmemory,optmethod,optbasis,optroute,specialopts,charge,multiplicity):
        '''write input file and input list for each 10 conformers to optimize'''

        for i in range(1, 11):
            com_name = '{0}/{1}-conf{2}.com'.format(conf_opt_dir, title, i)
            chk_name = '{0}-conf{1}.chk'.format(title, i)
            write_com(com_name,chk_name,optcores,optmemory,optmethod,optbasis,optroute,specialopts,charge,multiplicity)

            if i == 1:
                with open('{0}/{1}-coms.txt'.format(conf_opt_dir, title), 'w') as coms:
                    coms.write('{0}-conf{1}.com\n'.format(title, i))
            else:
                with open('{0}/{1}-coms.txt'.format(conf_opt_dir, title), 'a') as coms:
                    coms.write('{0}-conf{1}.com\n'.format(title, i))


    def _sbatch(tmptitle,optpartition,optcores,optmemory,opttime,conf_opt_dir,title,charge,multiplicity,conf_search_dir,g16root):
        '''Write conformer submission script'''

        sbatch="""#!/bin/bash
#SBATCH --job-name={0}-confopt
#SBATCH --output={5}/out.o
#SBATCH --error={5}/out.e
#SBATCH --partition={1}
#SBATCH --nodes=1
#SBATCH --ntasks={2}
#SBATCH --mem={3}G
#SBATCH --time={4}
#SBATCH --array=1-10
hostname
work={5}
cd $work


if [[ ${{SLURM_ARRAY_TASK_ID}} -eq 1 ]]
    then
    if test -f {6}-complete
        then
        rm {6}-complete
        rm {6}-energies.txt
        sed -i '1,/{7} {8}/!d' {6}-conf*com
        for i in {6}-conf*com
            do
            old=$(grep "%oldchk=" -c $i)
            if [[ $old -gt 0 ]]
                then
                sed -i 1d $i
                sed -i 's/geom=check//g' $i
                sed -i 's/guess=read//g' $i
                sed -i 's/readfc/calcfc/g' $i
            fi
        done     
    fi
    
    nstruct=$(ls -la {9}/{6}/ORCA/{6}-all-sorted-conf*.xyz |wc -l)
    for ((x=1;x<=nstruct;x++)); do  
        energy=$(tac {9}/{6}/ORCA/{6}-conf$x.out | grep "FINAL SINGLE POINT ENERGY" -m1)
        echo $energy >> {6}-complete
        awk "/FINAL SINGLE POINT ENERGY/{{i++}}i==$x{{print ; exit}}" {6}-complete | awk '{{ print $5}}' >> {6}-energies.txt; done
    awk '{{print NR "   "  $s}}' {6}-energies.txt > {6}-output.txt
    sort -k2n {6}-output.txt > {6}-energies-sorted.txt
    lowest10=$(awk  '{{print $1}} NR==10{{exit}}' {6}-energies-sorted.txt )
    count=0
    for b in $lowest10
        do
        echo $lowest10
        count=$((count+1))
        python3 ../utilities/orca2xyz.py {9}/{6}/ORCA/{6}-conf$b.out {6}-conf$count.xyz
        tail -n +3 {6}-conf$count.xyz >> {6}-conf$count.com
        echo " " >> {6}-conf$count.com
    done
    sbatch --dependency=afterok:$SLURM_ARRAY_JOB_ID ../lowest_ts/{6}-lowest.sbatch
    sbatch --dependency=afternotok:$SLURM_ARRAY_JOB_ID {6}-failed.sbatch
    time=$(date)
    echo "$SLURM_JOB_NAME $time" >> ../status.txt
else
    sleep 120s
fi

nconf=$(cat {6}-energies-sorted.txt |wc -l)

if [[ ${{SLURM_ARRAY_TASK_ID}} -le $nconf ]]
    then
    input=$(sed "${{SLURM_ARRAY_TASK_ID}}q;d" {6}-coms.txt)
    export INPUT=$input
    export WORKDIR=$work
    export GAUSS_SCRDIR=$work
    export g16root={10}
    . $g16root/g16/bsd/g16.profile

    cd $WORKDIR
    $g16root/g16/g16 $INPUT
 
    station=$(grep "Station" -c ${{INPUT%.*}}.log)
    if [[ $station -lt 2 ]]
       then
       exit 1234
    fi
  
    freq=$(tac ${{INPUT%.*}}.log | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
    if [[ $freq -gt 1 ]]
        then 
        exit 1234
    fi



else
    echo "no ${{SLURM_ARRAY_TASK_ID}}'th conformer generated" >> ../lowest_ts/{6}-lowest_ts-energies.txt
    #rm {6}-conf$SLURM_ARRAY_TASK_ID.com
fi

""".format(tmptitle,optpartition,optcores,optmemory,opttime,conf_opt_dir,title,charge,multiplicity,conf_search_dir,g16root)
        with open('{0}/{1}-submit.sbatch'.format(conf_opt_dir,title),'w') as batch:
            batch.write(sbatch)


# failed script for conf opt - resubmits the failed jobs, up to 3 times
    def _failed(tmptitle,short_partition,conf_opt_dir,title,charge,multiplicity,lowest_ts_dir,errorlog):
        '''Failed script for conformer optimizations, allow up to 3 re-submisions'''

        failed=r"""#!/bin/bash
#SBATCH --job-name={0}-conf_opt-failed
#SBATCH --output={2}/resubmit.o
#SBATCH --error={2}/resubmit.e
#SBATCH --partition={1}
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --time=00:20:00
hostname

work={2}
cd $work
touch failed-script-ran
time=$(date)
echo "$SLURM_JOB_NAME $time" >> ../status.txt
if test -f {3}-resubmit.txt
    then
    nresub=$(sed "1q;d" {3}-resubmit.txt)
else
    nresub=0
fi
nresub=$((nresub+=1))
if [[ $nresub -lt 3 ]]
    then
    rm {3}-resubmit.txt
    echo $nresub >> {3}-resubmit.txt
    for i in {0}-conf*log
        do
        finished=$(grep 'Station' -c $i)
        freq=$(tac $i | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
        if [[ $finished -lt 2 ]]
            then
            convert=$(obabel $i -o xyz)
            if [[ $convert == *"0 molecules converted"* ]]
                then
                echo "${{i%.*}} could not be converted, reverting to original" >> {3}-resublog.txt
                old=$(grep "%oldchk=" -c ${{i%.*}}.com)
                sed -i '1,/{4} {5}/!d' ${{i%.*}}.com
                echo " " ${{i%.*}}.com
                if [[ $old -gt 0 ]]
                    then
                    sed -i 1d ${{i%.*}}.com
                fi
                sed -i 's/geom=check//g' ${{i%.*}}.com
                sed -i 's/guess=read//g' ${{i%.*}}.com
                sed -i 's/opt=(readfc,ts,noeigen/opt=(calcfc,ts,noeigen/g' ${{i%.*}}.com
                end=${{i#-conf*}}
                index=${{end%.*}} 
                tail -n +3 {0}-conf$index.xyz >> ${{i%.*}}.com
                echo " " >>  ${{i%.*}}.com
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
                echo "${{i%.*}} Non-stationary point found, reading previous fc" >> {3}-resublog.txt
                echo " " >> ${{i%.*}}.com
                if [[ $old -gt 0 ]]
                    then
                    sed -i 1d ${{i%.*}}.com
                fi
                sed -i 's/geom=check//g' ${{i%.*}}.com
                sed -i 's/guess=read//g' ${{i%.*}}.com
                mv ${{i%.*}}.chk ${{i%.*}}-readingfc.chk
                sed -i 's/opt=(calcfc,ts,noeigen/opt=(readfc,ts,noeigen/g' ${{i%.*}}.com
                sed -i 's/freq=noraman/freq=noraman geom=check guess=read/g' ${{i%.*}}.com
                sed -i "1s/^/%oldchk=${{i%.*}}-readingfc.chk\n/" ${{i%.*}}.com
                echo " " >> ${{i%.*}}.com

             #stationary found, but didnt finish frequencies or far from starting geometry
                 #re-calculate force constants
             elif ([[ $finished -eq 1 ]] && [[ $termination -lt 2 ]]) || ([[ $cycles -gt 15 ]])
                then
                echo "${{i%.*}} failed frequencies or is far from input geometry" >> {3}-resublog.txt
                if [[ $old -gt 0 ]]
                    then
                    sed -i 1d ${{i%.*}}.com
                fi
                obabel $i -o xyz | tail -n +3 >> ${{i%.*}}.com
                echo " " >> ${{i%.*}}.com
                sed -i 's/geom=check//g' ${{i%.*}}.com
                sed -i 's/guess=read//g' ${{i%.*}}.com
                sed -i 's/opt=(readfc,ts,noeigen/opt=(calcfc,ts,noeigen/g' ${{i%.*}}.com
                echo " " >> ${{i%.*}}.com

             #no stationary point found yet
             else
                fc=$(grep "Converged?" -c $i)
  
                #if force constants were finished computing, read them
                if [[ $fc -gt 0 ]]
                    then
                    echo "${{i%.*}} did not find stationary point, reading fc" >> {3}-resublog.txt
                    echo " " >> ${{i%.*}}.com
                    if [[ $old -gt 0 ]]
                        then
                        sed -i 1d ${{i%.*}}.com
                    fi
                    sed -i 's/geom=check//g' ${{i%.*}}.com
                    sed -i 's/guess=read//g' ${{i%.*}}.com
                    mv ${{i%.*}}.chk ${{i%.*}}-readingfc.chk
                    sed -i 's/opt=(calcfc,ts,noeigen/opt=(readfc,ts,noeigen/g' ${{i%.*}}.com
                    sed -i 's/freq=noraman/freq=noraman geom=check guess=read/g' ${{i%.*}}.com
                    sed -i "1s/^/%oldchk=${{i%.*}}-readingfc.chk\n/" ${{i%.*}}.com
                    echo " " >> ${{i%.*}}.com
                 #if not, take geometry and restart
                 else
                    echo "${{i%.*}} did not find stationary point and has no fc" >> {3}-resublog.txt
                    obabel $i -o xyz |tail -n +3 >> ${{i%.*}}.com
                    echo " " >> ${{i%.*}}.com
                    if [[ $old -gt 0 ]]
                        then
                        sed -i 1d ${{i%.*}}.com
                    fi
                    sed -i 's/geom=check//g' ${{i%.*}}.com
                    sed -i 's/guess=read//g' ${{i%.*}}.com
                    sed -i 's/opt=(readfc,ts,noeigen/opt=(calcfc,ts,noeigen/g' ${{i%.*}}.com 
                    echo " " >> ${{i%.*}}.com
                fi
            fi
            fi
        echo ${{i%.*}}.com >> {3}-resubmit.txt
        echo " " >> ${{i%.*}}.com

    elif [[ $finished -gt 1 ]] && [[ $freq -gt 1 ]]
        then
             #stationary found, but its a saddle point
                 #re-calculate force constants
            echo "${{i%.*}} Saddle point found" >> {3}-resublog.txt
            old=$(grep "%oldchk=" -c ${{i%.*}}.com)
            sed -i '1,/{4} {5}/!d' ${{i%.*}}.com
            if [[ $old -gt 0 ]]
                then
                sed -i 1d ${{i%.*}}.com
            fi
            obabel $i -o xyz | tail -n +3 >> ${{i%.*}}.com
            echo " " >> ${{i%.*}}.com
            sed -i 's/geom=check//g' ${{i%.*}}.com
            sed -i 's/guess=read//g' ${{i%.*}}.com
            sed -i 's/opt=(readfc,ts,noeigen/opt=(calcfc,ts,noeigen/g' ${{i%.*}}.com
            echo " " >> ${{i%.*}}.com
            echo ${{i%.*}}.com >> {3}-resubmit.txt
            echo " " >> ${{i%.*}}.com

    fi
    done
    toresub=$(cat {3}-resubmit.txt |wc -l)
    sed -i "s/#SBATCH --array=.*/#SBATCH --array=2-$toresub/g" {3}-submit.sbatch
    sed -i "s/{3}-coms.txt/{3}-resubmit.txt/g" {3}-submit.sbatch
    ID=$(sbatch --parsable {3}-submit.sbatch)
    sbatch --dependency=afterok:$ID  {6}/{3}-lowest.sbatch
    sbatch --dependency=afternotok:$ID {3}-failed.sbatch
else
    if test -f {3}-NEEDS_MANUAL_FIX.txt
        then
        rm {3}-NEEDS_MANUAL_FIX.txt
    fi
    echo 'Falied too many times and need manual attention - re-submit with {3}-submit.sbatch after making changes' >> {3}-NEEDS_MANUAL_FIX.txt

    for i in {3}-conf*log
        do
        finished=$(grep 'Station' -c $i)
        if [[ $finished -lt 2 ]]
            then
            echo ${{i%.*}}.com >> {3}-NEEDS_MANUAL_FIX.txt

        else
            freq=$(tac $i | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
            if [[ $freq -gt 1 ]]
                then 
                echo ${{i%.*}}.com >> {3}-NEEDS_MANUAL_FIX.txt
            fi
        fi
    done
    toresub=$(cat {3}-NEEDS_MANUAL_FIX.txt |wc -l)
        if [[ $toresub == 1 ]]
            then
            sbatch --parsable {6}/{3}-lowest.sbatch
        fi
    sed -i "s/#SBATCH --array=.*/#SBATCH --array=2-$toresub/g" {3}-submit.sbatch
    sed -i "s/{3}-resubmit.txt/{3}-NEEDS_MANUAL_FIX.txt/g" {3}-submit.sbatch
    echo "{3} failed too many times. RUN TERMINATED" >> ../status.txt
    echo "{3} failed too many times. RUN TERMINATED" >> {7}/{3}

fi
""".format(tmptitle,short_partition,conf_opt_dir,title,charge,multiplicity,lowest_ts_dir,errorlog)
        with open('{0}/{1}-failed.sbatch'.format(conf_opt_dir,title),'w') as batch:
            batch.write(failed)

########################################################
# Extracting lowest energy TS and Benchmarking Scripts #
########################################################

#get the lowest enregy TS and set up benchmarking if requried
def getlowest(title,conf_opt_dir,utilities_dir,benchmark,runlog,short_partition,tmptitle,irc,c1,a1,a2,c2,lowest_ts_dir):
    '''Grab lowest energy TS and start benchmarking if applicable'''

    if benchmark:
        lowest="""#!/bin/bash
#SBATCH --job-name={3}-getlowbench
#SBATCH --output={10}/out.o
#SBATCH --error={10}/out.e
#SBATCH --partition={5}
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --time=10:00
hostname

work={1}
cd $work
time=$(date)
echo "$SLURM_JOB_NAME $time"  >> ../status.txt
echo "$SLURM_JOB_NAME autots reached endpoint. Lowest ts in $work at $time" >> {4}/{0}
if test -f {0}-ts-energies.txt 
    then 
    rm {0}-ts-energies.txt
fi
if test -f {0}-coms.txt
    then
    rm {0}-coms.txt
fi

#old bash get_lowest script
#bash {2}/get-lowest.sh {0} conf_opt

#new python get_lowest script (also calculates dihedrals to filter more bad TS structures)
python3 ../utilities/get_lowest.py {0} {6} {7} {8} {9} conf_opt

cd ../lowest_ts

success=$(ls -la {0}.log | wc -l)
if [[ $success -lt 1 ]]
    then
    echo "No valid TS structure generated for {0} - check the conformer geometries" >> ../status.txt
    exit 1234
fi

#get coordinates
obabel {0}.log -o xyz -O {0}.xyz

sbatch --parsable ../benchmarking/{0}-tier0.sbatch

""".format(title,conf_opt_dir,utilities_dir,tmptitle,runlog,short_partition,c1,a1,a2,c2,lowest_ts_dir)

    else:
        if irc:
        #needs to submit the sbatch in the irc dir
            lowest="""#!/bin/bash
#SBATCH --job-name={4}-getlow
#SBATCH --output={11}/out.o
#SBATCH --error={11}/out.e
#SBATCH --partition={6}
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --time=10:00
hostname
work={1}
cd $work
time=$(date)
echo "$SLURM_JOB_NAME $time" >> ../status.txt
echo "$SLURM_JOB_NAME autots ended TS search. Lowest TS in $work at $time" >> {5}/{0}
if test -f {3}-ts-energies.txt
    then
    rm {3}-ts-energies.txt
fi

#old bash get_lowest script
#bash {2}/get-lowest.sh {0} conf_opt

#new python get_lowest script (also calculates dihedrals to filter more bad TS structures)
python3 ../utilities/get_lowest.py {0} {7} {8} {9} {10} conf_opt


cd ../lowest_ts

success=$(ls -la {0}.log | wc -l)
if [[ $success -lt 1 ]]
    then
    echo "No valid TS structure generated for {0} - check the conformer geometries" >> ../status.txt
    exit 1234
fi

obabel {3}.log -o xyz -O {3}.xyz

sbatch  --parsable ../irc/{0}-submit.sbatch

""".format(title,conf_opt_dir,utilities_dir,title,tmptitle,runlog,short_partition,c1,a1,a2,c2,lowest_ts_dir)

        else:
            #no further calculations
            lowest="""#!/bin/bash
#SBATCH --job-name={4}-getlow
#SBATCH --output={11}/out.o
#SBATCH --error={11}/out.e
#SBATCH --partition={6}
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --time=10:00
hostname
work={1}
cd $work
time=$(date)
echo "$SLURM_JOB_NAME $time" >> ../status.txt
echo "$SLURM_JOB_NAME autots ended TS search. Lowest TS in $work at $time" >> {5}/{0}
if test -f {3}-ts-energies.txt
    then
    rm {3}-ts-energies.txt
fi

#old bash get_lowest script
#bash {2}/get-lowest.sh {3} conf_opt

#new python get_lowest script (also calculates dihedrals to filter more bad TS structures)
python3 ../utilities/get_lowest.py {3} {7} {8} {9} {10} conf_opt


cd ../lowest_ts

success=$(ls -la {0}.log | wc -l)
if [[ $success -lt 1 ]]
    then
    echo "No valid TS structure generated for {0} - check the conformer geometries" >> ../status.txt
    exit 1234
fi

obabel {3}.log -o xyz -O {3}.xyz

""".format(title,conf_opt_dir,utilities_dir,title,tmptitle,runlog,short_partition,c1,a1,a2,c2,lowest_ts_dir)


    with open('{0}/{1}-lowest.sbatch'.format(lowest_ts_dir,title),'w') as batch:
        batch.write(lowest)


####################
### Benchmarking ###
####################
class benchmarking():

    def _input(benchmarkmethods,benchmarkbasis,benchmark_dir,title,optmethod,optcores,optmemory,optbasis,optroute,charge,multiplicity):
        '''Write the benchmarking input files'''

        #make sure the com lists are cleared
        length_of_tiers = [len(basislist) for basislist in benchmarkbasis]
        max_tier = np.amax(length_of_tiers) 
        for tier in range(0,max_tier):
            if os.path.exists('{0}/{1}-tier{2}.txt'.format(benchmark_dir,title,tier)):
                os.remove('{0}/{1}-tier{2}.txt'.format(benchmark_dir,title,tier))

        for x,method in enumerate(benchmarkmethods):
            for basislist in benchmarkbasis:
                for tier,optbasis in enumerate(basislist):
                    specialopts = method[1]
                    optmethod = method[0]
                    com_name = '{0}/{1}-{2}-{3}-tier{4}.com'.format(benchmark_dir,title,optmethod,basis_dict[optbasis],tier)
                    chk_name = '{0}-{1}-{2}-tier{3}.chk'.format(title,optmethod,basis_dict[optbasis],tier)
                    write_benchmarking_com(com_name,chk_name,optcores[tier],optmemory[tier],optmethod,optbasis,optroute,specialopts,charge,multiplicity,tier,basislist,title,'lowest_ts','')
                    with open('{0}/{1}-tier{2}.txt'.format(benchmark_dir,title,tier),'a') as coms:
                        coms.write('{0}-{1}-{2}-tier{3}.com\n'.format(title,optmethod,basis_dict[optbasis],tier))

    def _sbatch_template(tmptitle,tier,optpartition,optcores,optmemory,opttime,ncalcs,benchmark_dir,title,next_tier,g16root):
        '''Write the benchmarking sbatch'''    

        sbatch="""#!/bin/bash
#SBATCH --job-name={0}-tier{1}
#SBATCH --output={7}/out.o
#SBATCH --error={7}/out.e
#SBATCH --partition={2}
#SBATCH --nodes=1
#SBATCH --ntasks={3}
#SBATCH --mem={4}G
#SBATCH --time={5}
#SBATCH --array=1-{6}%50
hostname
work={7}
cd $work

if [[ $SLURM_ARRAY_TASK_ID == 1 ]]
    then
    if  [[ ! -f ../lowest_ts/{8}.chk  ]]
        then
        echo "No valid TS found in conformer optimization - check lowest_ts/{8}-ts-energies.csv" >> ../status.txt
        exit 1234
    fi
    time=$(date)
    echo "$SLURM_JOB_NAME $time" >> ../status.txt

    ID=$SLURM_ARRAY_JOB_ID
    if test -f {8}-tier{9}.sbatch
        then
        sbatch --dependency=afterok:$ID {8}-tier{9}.sbatch
    fi
    sbatch --dependency=afterok:$ID ../irc/{8}-tier{1}.sbatch
    sbatch --dependency=afternotok:$ID {8}-tier{1}-failed.sbatch
fi
input=$(sed "${{SLURM_ARRAY_TASK_ID}}q;d" {8}-tier{1}.txt)
export INPUT=$input
export WORKDIR=$work
export GAUSS_SCRDIR=$work
export g16root={10}
. $g16root/g16/bsd/g16.profile
cd $WORKDIR
$g16root/g16/g16 $INPUT

station=$(grep "Station" -c ${{INPUT%.*}}.log)
if [[ $station -lt 2 ]]
    then
    exit 1234
fi

freq=$(tac ${{INPUT%.*}}.log | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
if [[ $freq -gt 1 ]]
    then 
    exit 1234
fi



""".format(tmptitle,tier,optpartition,optcores,optmemory,opttime,ncalcs,benchmark_dir,title,next_tier,g16root)
        return(sbatch)

    def _sbatch(benchmarkbasis,tmptitle,optpartition,optcores,optmemory,opttime,benchmark_dir,title,g16root):
        '''write the template sbatch for each tier'''

        length_of_tiers = [len(basislist) for basislist in benchmarkbasis]
        max_tier = np.amax(length_of_tiers) 
    
        for tier in range(0,max_tier):
            nbasis = 0
            for tierlength in length_of_tiers:
                if tier < tierlength:
                    nbasis +=1
            ncalcs = nbasis * len(benchmarkmethods)
            with open('{0}/{1}-tier{2}.sbatch'.format(benchmark_dir,title,tier),'w') as batch:
                batch.write(benchmarking._sbatch_template(tmptitle,tier,optpartition,optcores[tier],optmemory[tier],opttime,ncalcs,benchmark_dir,title,tier+1,g16root))
        

    def _failed_template(tmptitle,short_partition,benchmark_dir,title,tier,charge,multiplicity,next_tier,errorlog):
        '''failure script for benchmarking'''

        sbatch=r"""#!/bin/bash
#SBATCH --job-name={0}-benchmark-failed
#SBATCH --output={2}/resubmit.o
#SBATCH --error={2}/resubmit.e
#SBATCH --partition={1}
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --time=00:20:00
hostname

work={2}
cd $work
echo $SLURM_JOB_NAME >> ../status.txt
touch failed-script-ran

if test -f {3}-tier{4}-resubmit.txt
    then
    nresub=$(sed "1q;d" {3}-tier{4}-resubmit.txt)
else
    nresub=0
fi
nresub=$((nresub+=1))
if [[ $nresub -lt 3 ]]
    then
    rm {3}-tier{4}-resubmit.txt
    echo $nresub >> {3}-tier{4}-resubmit.txt
    for i in {3}-*-tier{4}.log
        do
        echo "READING FILE $i" >>{3}-tier{4}-resublog.txt
        finished=$(grep 'Station' -c $i)
        freq=$(tac $i | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
        scf=$(grep "SCF Error SCF Error SCF Error SCF Error" $i -c )
        if [[ $finished -lt 2 ]]
            then
            convert=$(obabel $i -o xyz)
            if [[ $convert == *"0 molecules converted"* ]]
                then
                echo "${{i%.*}} did not reach restart point, or failed terribly" >> {3}-tier{4}-resublog.txt
                old=$(grep "%oldchk=" -c ${{i%.*}}.com)
                sed -i '1,/{5} {6}/!d' ${{i%.*}}.com
                echo " " >> ${{i%.*}}.com
                if [[ $old -gt 0 ]]
                    then
                    sed -i 1d ${{i%.*}}.com
                fi
                sed -i 's/geom=check//g' ${{i%.*}}.com
                sed -i 's/guess=read//g' ${{i%.*}}.com
                sed -i 's/,maxstep=10//g' ${{i%.*}}.com
                sed -i 's/opt=(calcfc,ts,noeigen)/opt=(calcfc,ts,noeigen,maxstep=10)/g' ${{i%.*}}.com
                sed -i 's/opt=(readfc,ts,noeigen)/opt=(calcfc,ts,noeigen,maxstep=10)/g' ${{i%.*}}.com 
                tail -n +3 ../lowest_ts/{3}.xyz >> ${{i%.*}}.com 
                echo " " >>  ${{i%.*}}.com
                echo '--Link1--' >>  ${{i%.*}}.com
                top=$(head -n 8 ${{i%.*}}.com)
                echo -ne "${{top/opt=(calcfc,ts,noeigen,maxstep=10)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                echo " " >>  ${{i%.*}}.com

            #SCF Convergence issues
            elif [[ $scf -gt 0 ]]
                then
                echo "${{i%.*}} SCF failed to converge, using scf=qc" >> {3}-tier{4}-resublog.txt
                sed -i 's/opt/scf=qc opt/g' ${{i%.*}}.com
            else

            sed -i '1,/{5} {6}/!d' ${{i%.*}}.com
            termination=$(grep "Normal termination" -c $i)
            cycles=$(grep "SCF Done" -c $i)
            check=$(grep "geom=check guess=read" -c ${{i%.*}}.com)
            
            old=$(grep "%oldchk=" -c ${{i%.*}}.com)

            #Non stationary point found
                 #read in fc
            if [[ $finished -eq 1 ]] && [[ $termination -ge 2 ]]
                then
                echo "${{i%.*}} finished with non-stationary point, reading previous fc" >> {3}-tier{4}-resublog.txt
                echo " " ${{i%.*}}.com
                if [[ $old -gt 0 ]]
                    then
                    sed -i 1d ${{i%.*}}.com
                fi
                sed -i 's/geom=check//g' ${{i%.*}}.com
                sed -i 's/guess=read//g' ${{i%.*}}.com
                sed -i 's/,maxstep=10//g' ${{i%.*}}.com
                mv ${{i%.*}}.chk ${{i%.*}}-readingfc.chk
                echo " " >>  ${{i%.*}}.com
                echo '--Link1--' >>  ${{i%.*}}.com
                sed -i 's/opt=(readfc,ts,noeigen)/opt=(readfc,ts,noeigen,maxstep=10)/g' ${{i%.*}}.com
                sed -i 's/opt=(calcfc,ts,noeigen)/opt=(readfc,ts,noeigen,maxstep=10)/g' ${{i%.*}}.com
                top=$(head -n 8 ${{i%.*}}.com)
                echo -ne "${{top/opt=(readfc,ts,noeigen,maxstep=10)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                sed -i 's/opt=(readfc,ts,noeigen,maxstep=10)/opt=(readfc,ts,noeigen,maxstep=10) geom=check guess=read/g' ${{i%.*}}.com
                sed -i "1s/^/%oldchk=${{i%.*}}-readingfc.chk\n/" ${{i%.*}}.com
                echo " " >>${{i%.*}}.com
 
             #stationary found, but didnt finish frequencies or far from starting geometry
                 #re-calculate force constants
             elif ([[ $finished -eq 1 ]] && [[ $termination -lt 2 ]]) || ([[ $cycles -gt 15 ]])
                then
                echo "${{i%.*}} didnt finish freq, or is far from starting geometry" >> {3}-tier{4}-resublog.txt
                if [[ $old -gt 0 ]]
                    then
                    sed -i 1d ${{i%.*}}.com
                fi
                obabel $i -o xyz | tail -n +3 >> ${{i%.*}}.com
                sed -i 's/geom=check//g' ${{i%.*}}.com
                sed -i 's/guess=read//g' ${{i%.*}}.com
                sed -i 's/,maxstep=10//g' ${{i%.*}}.com
                sed -i 's/opt=(calcfc,ts,noeigen)/opt=(calcfc,ts,noeigen,maxstep=10)/g' ${{i%.*}}.com
                sed -i 's/opt=(readfc,ts,noeigen)/opt=(calcfc,ts,noeigen,maxstep=10)/g' ${{i%.*}}.com
                echo " " >> ${{i%.*}}.com
                echo '--Link1--' >>  ${{i%.*}}.com
                top=$(head -n 8 ${{i%.*}}.com)
                echo -ne "${{top/opt=(calcfc,ts,noeigen,maxstep=10)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                echo " " >>${{i%.*}}.com

             #no stationary point found yet
             else
                
                fc=$(grep "Converged?" -c $i)
  
                #if force constants were finished computing, read them
                if [[ $fc -gt 0 ]]
                    then
                    echo "${{i%.*}} no stationary point found, reading fc" >> {3}-tier{4}-resublog.txt
                    if [[ $old -gt 0 ]]
                        then
                        sed -i 1d ${{i%.*}}.com
                    fi
                    sed -i 's/geom=check//g' ${{i%.*}}.com
                    sed -i 's/guess=read//g' ${{i%.*}}.com
                    sed -i 's/,maxstep=10//g' ${{i%.*}}.com
                    mv ${{i%.*}}.chk ${{i%.*}}-readingfc.chk
                    sed -i 's/opt=(readfc,ts,noeigen)/opt=(readfc,ts,noeigen,maxstep=10)/g' ${{i%.*}}.com
                    sed -i 's/opt=(calcfc,ts,noeigen)/opt=(readfc,ts,noeigen,maxstep=10)/g' ${{i%.*}}.com
                    echo " " >> ${{i%.*}}.com
                    echo '--Link1--' >>  ${{i%.*}}.com
                    top=$(head -n 8 ${{i%.*}}.com)
                    echo -ne "${{top/opt=(readfc,ts,noeigen,maxstep=10)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                    sed -i 's/opt=(readfc,ts,noeigen,maxstep=10)/opt=(readfc,ts,noeigen,maxstep=10) geom=check guess=read/g' ${{i%.*}}.com
                    sed -i "1s/^/%oldchk=${{i%.*}}-readingfc.chk\n/" ${{i%.*}}.com
                    echo " " >>${{i%.*}}.com 

                 #if not, take geometry and restart
                 else
                    echo "${{i%.*}} no stationary point found, nor fc, starting again" >> {3}-tier{4}-resublog.txt
                    obabel $i -o xyz |tail -n +3 >> ${{i%.*}}.com
                    if [[ $old -gt 0 ]]
                        then
                        sed -i 1d ${{i%.*}}.com
                    fi
                    sed -i 's/geom=check//g' ${{i%.*}}.com
                    sed -i 's/guess=read//g' ${{i%.*}}.com
                    sed -i 's/,maxstep=10//g' ${{i%.*}}.com
                    sed -i 's/opt=(calcfc,ts,noeigen)/opt=(calcfc,ts,noeigen,maxstep=10)/g' ${{i%.*}}.com
                    sed -i 's/opt=(readfc,ts,noeigen)/opt=(calcfc,ts,noeigen,maxstep=10)/g' ${{i%.*}}.com 
                    echo " " >>${{i%.*}}.com
                    echo '--Link1--' >>  ${{i%.*}}.com
                    top=$(head -n 8 ${{i%.*}}.com)
                    echo -ne "${{top/opt=(calcfc,ts,noeigen,maxstep=10)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                    echo " " >>${{i%.*}}.com

                fi
            fi
            fi
        echo ${{i%.*}}.com >> {3}-tier{4}-resubmit.txt
        echo " " >> ${{i%.*}}.com

    elif [[ $finished -gt 1 ]] && [[ $freq -gt 1 ]]
        then
             #stationary found, but its a saddle point
                 #re-calculate force constants
            echo "${{i%.*}} Saddle point found" >> {3}-tier{4}-resublog.txt
            old=$(grep "%oldchk=" -c ${{i%.*}}.com)
            sed -i '1,/{5} {6}/!d' ${{i%.*}}.com
            if [[ $old -gt 0 ]]
                then
                sed -i 1d ${{i%.*}}.com
            fi
            obabel $i -o xyz | tail -n +3 >> ${{i%.*}}.com
            sed -i 's/geom=check//g' ${{i%.*}}.com
            sed -i 's/guess=read//g' ${{i%.*}}.com
            sed -i 's/,maxstep=10//g' ${{i%.*}}.com
            sed -i 's/opt=(calcfc,ts,noeigen)/opt=(calcfc,ts,noeigen,maxstep=10)/g' ${{i%.*}}.com
            sed -i 's/opt=(readfc,ts,noeigen)/opt=(calcfc,ts,noeigen,maxstep=10)/g' ${{i%.*}}.com
            echo " " >> ${{i%.*}}.com
            echo '--Link1--' >>  ${{i%.*}}.com
            top=$(head -n 8 ${{i%.*}}.com)
            echo -ne "${{top/opt=(calcfc,ts,noeigen,maxstep=10)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
            echo " " >>${{i%.*}}.com
            echo ${{i%.*}}.com >> {3}-tier{4}-resubmit.txt

   else
        echo "$i is done" >> {3}-tier{4}-resublog.txt
    fi
    
    done

    toresub=$(cat {3}-tier{4}-resubmit.txt |wc -l)
    sed -i "s/#SBATCH --array=.*/#SBATCH --array=2-$toresub/g" {3}-tier{4}.sbatch
    sed -i "s/{3}-tier{4}.txt/{3}-tier{4}-resubmit.txt/g" {3}-tier{4}.sbatch
    ID=$(sbatch --parsable {3}-tier{4}.sbatch)
    sbatch --dependency=afterok:$ID ../irc/{3}-tier{4}.sbatch
    sbatch --dependency=afternotok:$ID {3}-tier{4}-failed.sbatch

    if test -f {3}-tier{7}.sbatch
        then
        sbatch --dependency=afterok:$ID {3}-tier{7}.sbatch
    fi
else
    if test -f {3}-tier{4}-NEEDS_MANUAL_FIX.txt
        then
        rm {3}-tier{4}-NEEDS_MANUAL_FIX.txt
    fi
    echo 'Falied too many times and need manual attention - re-submit with {3}-tier{4}.sbatch after making changes' >> {3}-tier{4}-NEEDS_MANUAL_FIX.txt

    for i in {3}-*-tier{4}.log
        do
        finished=$(grep 'Station' -c $i)
        if [[ $finished -lt 2 ]]
            then
            echo ${{i%.*}}.com >> {3}-tier{4}-NEEDS_MANUAL_FIX.txt
        else
            freq=$(tac $i | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
            if [[ $freq -gt 1 ]]
                then 
                echo ${{i%.*}}.com >> {3}-tier{4}-NEEDS_MANUAL_FIX.txt
            fi 
        fi
    done
    toresub=$(cat {3}-tier{4}-NEEDS_MANUAL_FIX.txt |wc -l)
        if [[ $toresub == 1 ]]
            then
            sbatch ../irc/{3}-tier{4}.sbatch
            if test -f {3}-tier{7}.sbatch
                then
                sbatch {3}-tier{7}.sbatch
            fi
        fi

    sed -i "s/#SBATCH --array=.*/#SBATCH --array=2-$toresub/g" {3}-tier{4}.sbatch
    sed -i "s/{3}-tier{4}-resubmit.txt/{3}-tier{4}-NEEDS_MANUAL_FIX.txt/g" {3}-tier{4}.sbatch
    echo "{3} failed too many times. RUN TERMINATED" >> ../status.txt
    echo "{3} failed too many times. RUN TERMINATED" >> {8}/{3}

    #if test -f {3}-tier{7}.sbatch
    #    then
    #    sbatch {3}-tier{7}.sbatch
    #fi

fi
""".format(tmptitle,short_partition,benchmark_dir,title,tier,charge,multiplicity,next_tier,errorlog)
        return sbatch



    def _failed(tmptitle,short_partition,benchmark_dir,title,charge,multiplicity,errorlog,benchmarkbasis):
        '''write the failure script  from the template'''

        length_of_tiers = [len(basislist) for basislist in benchmarkbasis]
        max_tier = np.amax(length_of_tiers) 
    
        for tier in range(0,max_tier):
             with open('{0}/{1}-tier{2}-failed.sbatch'.format(benchmark_dir,title,tier),'w') as batch:
                 batch.write(benchmarking._failed_template(tmptitle,short_partition,benchmark_dir,title,tier,charge,multiplicity,tier+1,errorlog))

 
###########
### irc ###
###########
class IRC():
 #if the IRC is for benchmarking, need to make an IRC input for each method + basis, just like the benchmarking
    #if no benchmarking, just needs a single IRC for each molecule from the lowest_ts


    def _benchmarking_input(benchmarkmethods,benchmarkbasis,irc_dir,optcores,optmemory,ircroute_forward,ircroute_reverse,charge,multiplicity,title):
        '''Write the benchmarking irc input files'''

        #make sure the com lists are cleared
        length_of_tiers = [len(basislist) for basislist in benchmarkbasis]
        max_tier = np.amax(length_of_tiers) 
        for tier in range(0,max_tier):
            if os.path.exists('{0}/{1}-tier{2}.txt'.format(irc_dir,title,tier)):
                os.remove('{0}/{1}-tier{2}.txt'.format(irc_dir,title,tier))

        for x,method in enumerate(benchmarkmethods):
            for basislist in benchmarkbasis:
                for tier,optbasis in enumerate(basislist):
                    specialopts = method[1]
                    optmethod = method[0]
                    #forward
                    com_name_forward = '{0}/{1}-{2}-{3}-tier{4}-forward.com'.format(irc_dir,title,optmethod,basis_dict[optbasis],tier)
                    chk_name_forward = '{0}-{1}-{2}-tier{3}-forward.chk'.format(title,optmethod,basis_dict[optbasis],tier)
                    write_com(com_name_forward,chk_name_forward,optcores[tier],optmemory[tier],optmethod,optbasis,ircroute_forward,specialopts,charge,multiplicity)
                    #reverse
                    com_name_reverse = '{0}/{1}-{2}-{3}-tier{4}-reverse.com'.format(irc_dir,title,optmethod,basis_dict[optbasis],tier)
                    chk_name_reverse = '{0}-{1}-{2}-tier{3}-reverse.chk'.format(title,optmethod,basis_dict[optbasis],tier)
                    write_com(com_name_reverse,chk_name_reverse,optcores[tier],optmemory[tier],optmethod,optbasis,ircroute_reverse,specialopts,charge,multiplicity)

                    with open('{0}/{1}-tier{2}.txt'.format(irc_dir,title,tier),'a') as coms:
                        coms.write('{0}-{1}-{2}-tier{3}-forward.com\n'.format(title,optmethod,basis_dict[optbasis],tier))
                        coms.write('{0}-{1}-{2}-tier{3}-reverse.com\n'.format(title,optmethod,basis_dict[optbasis],tier))

    def _input(irc_dir,title,optcores,optmemory,optmethod,optbasis,ircroute_forward,ircroute_reverse,specialopts,charge,multiplicity):
        '''Write the input for just the lowest_ts IRC'''

        if os.path.exists('{0}/{1}-coms.txt'.format(irc_dir,title)):
            os.remove('{0}/{1}-coms.txt'.format(irc_dir,title))

        #forward
        com_name_forward = '{0}/{1}-forward.com'.format(irc_dir,title)
        chk_name_forward = '{0}-forward.chk'.format(title)
        write_com(com_name_forward,chk_name_forward,optcores,optmemory,optmethod,optbasis,ircroute_forward,specialopts,charge,multiplicity)
       
        #reverse
        com_name_reverse = '{0}/{1}-reverse.com'.format(irc_dir,title)
        chk_name_reverse = '{0}-reverse.chk'.format(title)
        write_com(com_name_reverse,chk_name_reverse,optcores,optmemory,optmethod,optbasis,ircroute_reverse,specialopts,charge,multiplicity)
        
        with open('{0}/{1}-coms.txt'.format(irc_dir,title),'a') as coms:
            coms.write('{0}-reverse.com\n'.format(title))
            coms.write('{0}-forward.com\n'.format(title))


        
    def _benchmarking_sbatch_template(tmptitle,tier,optpartition,optcores,optmemory,opttime,ncalcs,irc_dir,title,g16root):
        '''write sbatch to submit tier of IRC calcs'''
    
        sbatch=r"""#!/bin/bash
#SBATCH --job-name={0}-tier{1}-IRC
#SBATCH --output={7}/out.o
#SBATCH --error={7}/out.e
#SBATCH --partition={2}
#SBATCH --nodes=1
#SBATCH --ntasks={3}
#SBATCH --mem={4}G
#SBATCH --time={5}
#SBATCH --array=1-{6}%50
hostname
work={7}
cd $work

if [[ $SLURM_ARRAY_TASK_ID == 1 ]]
    then
    time=$(date)
    echo "$SLURM_JOB_NAME $time" >> ../status.txt

    #Submit reactant optimizations
    ID=$SLURM_ARRAY_JOB_ID
    sbatch --dependency=afterok:$ID ../reactants/{8}-tier{1}.sbatch
    
    #get force constants/geometries
    for i in {8}-*-tier{1}-forward.com
        do
        old=$(grep "%oldchk=" -c $i)
        if [[ $old -gt 0 ]]
            then
            sed -i 1d $i
        fi
        station=$(grep "Station" -c ../benchmarking/${{i%-forward*}}.log)
        if [[ $station -gt 1 ]]
            then
            freq=$(tac ../benchmarking/${{i%-forward*}}.log | grep "imaginary frequencies (negative Signs)"  -m1  |awk '{{ print $2 }}' )
            if [[ $freq -lt 2 ]]
                then 
                echo " " >> $i
                #add oldchk line
                sed -i "1s#^#%oldchk=../benchmarking/${{i%-forward*}}.chk\n#" $i
            else
                echo "$i failed freq check with $freq"
            fi
        else
            echo "$i failed station check with $station"
        fi
     done

    for i in {8}-*-tier{1}-reverse.com
        do
        old=$(grep "%oldchk=" -c $i)
        if [[ $old -gt 0 ]]
            then
            sed -i 1d $i
        fi
        station=$(grep "Station" -c ../benchmarking/${{i%-reverse*}}.log)
        if [[ $station -gt 1 ]]
            then
            freq=$(tac ../benchmarking/${{i%-reverse*}}.log | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
            if [[ $freq -lt 2 ]]
                then
                echo " " >> $i
                #add oldchk line
                sed -i "1s#^#%oldchk=../benchmarking/${{i%-reverse*}}.chk\n#" $i
            else
                echo "$i failed freq check with $freq"
            fi
        else
            echo "$i failed station check with $station"
        fi
     done

        
else
    sleep 120s
fi

input=$(sed "${{SLURM_ARRAY_TASK_ID}}q;d" {8}-tier{1}.txt)
export INPUT=$input
export WORKDIR=$work
export GAUSS_SCRDIR=$work
export g16root={9}
. $g16root/g16/bsd/g16.profile
cd $WORKDIR
$g16root/g16/g16 $INPUT

""".format(tmptitle,tier,optpartition,optcores,optmemory,opttime,ncalcs*2,irc_dir,title,g16root)
        return(sbatch)

    def _benchmarking_sbatch(benchmarkbasis,tmptitle,optpartition,optcores,optmemory,opttime,irc_dir,title,g16root):
        '''write the template sbatch for each tier'''

        length_of_tiers = [len(basislist) for basislist in benchmarkbasis]
        max_tier = np.amax(length_of_tiers) 
    
        for tier in range(0,max_tier):
            nbasis = 0
            for tierlength in length_of_tiers:
                if tier < tierlength:
                    nbasis +=1
            ncalcs = nbasis * len(benchmarkmethods)
            with open('{0}/{1}-tier{2}.sbatch'.format(irc_dir,title,tier),'w') as batch:
                batch.write(IRC._benchmarking_sbatch_template(tmptitle,tier,optpartition,optcores[tier],optmemory[tier],opttime,ncalcs,irc_dir,title,g16root))
          
    def _sbatch(tmptitle,optpartition,optcores,optmemory,opttime,irc_dir,title,g16root):
        '''write sbatch to submit tier of IRC calcs'''
    
        sbatch=r"""#!/bin/bash
#SBATCH --job-name={0}-IRC
#SBATCH --output={5}/out.o
#SBATCH --error={5}/out.e
#SBATCH --partition={1}
#SBATCH --nodes=1
#SBATCH --ntasks={2}
#SBATCH --mem={3}G
#SBATCH --time={4}
#SBATCH --array=1-2

hostname
work={5}
cd $work
if [[ $SLURM_ARRAY_TASK_ID == 1 ]]
    then

    time=$(date)
    echo "$SLURM_JOB_NAME $time" >> ../status.txt

    #Submit reactant optimizations
    ID=$SLURM_ARRAY_JOB_ID
    sbatch --dependency=afterok:$ID ../reactants/{6}-submit.sbatch
    
    #get force constants/geometries
        old=$(grep "%oldchk=" -c {6}-forward.com)
        if [[ $old -gt 0 ]]
            then
            sed -i 1d $i
        fi
        station=$(grep "Station" -c ../lowest_ts/{6}.log)
        if [[ $station -gt 1 ]]
            then
            freq=$(tac ../lowest_ts/{6}.log | grep "imaginary frequencies (negative Signs)"  -m1  |awk '{{ print $2 }}' )
            if [[ $freq -lt 2 ]]
                then 
                #add oldchk line
                sed -i "1s#^#%oldchk=../lowest_ts/{6}.chk\n#" {6}-forward.com
            else
                echo "../lowest_ts/{6}.log failed freq check with $freq"
            fi
        else
            echo "../lowest_ts/{6}.log failed station check with $station"
        fi

        old=$(grep "%oldchk=" -c {6}-reverse.com)
        if [[ $old -gt 0 ]]
            then
            sed -i 1d $i
        fi
        station=$(grep "Station" -c ../lowest_ts/{6}.log)
        if [[ $station -gt 1 ]]
            then
            freq=$(tac ../lowest_ts/{6}.log | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
            if [[ $freq -lt 2 ]]
                then
                #add oldchk line
                sed -i "1s#^#%oldchk=../lowest_ts/{6}.chk\n#" {6}-reverse.com
            else
                echo "../lowest_ts/{6}.log failed freq check with $freq"

            fi
        else
            echo "../lowest_ts/{6}.log failed station check with $station"

        fi


else
    sleep 120s
fi

input=$(sed "${{SLURM_ARRAY_TASK_ID}}q;d" {6}-coms.txt)
export INPUT=$input
export WORKDIR=$work
export GAUSS_SCRDIR=$work
export g16root={7}
. $g16root/g16/bsd/g16.profile
cd $WORKDIR
$g16root/g16/g16 $INPUT


""".format(tmptitle,optpartition,optcores,optmemory,opttime,irc_dir,title,g16root)
        with open('{0}/{1}-submit.sbatch'.format(irc_dir,title), 'w') as batch:
            batch.write(sbatch)


    def _benchmarking_reactants_input(benchmarkmethods,benchmarkbasis,reactants_dir,optcores,optmemory,optroute_reactants,charge,multiplicity,title):
        '''Write the benchmarking irc input files'''

        #make sure the com lists are cleared
        length_of_tiers = [len(basislist) for basislist in benchmarkbasis]
        max_tier = np.amax(length_of_tiers) 
        for tier in range(0,max_tier):
            if os.path.exists('{0}/{1}-tier{2}.txt'.format(reactants_dir,title,tier)):
                os.remove('{0}/{1}-tier{2}.txt'.format(reactants_dir,title,tier))

        for x,method in enumerate(benchmarkmethods):
            for basislist in benchmarkbasis:
                for tier,optbasis in enumerate(basislist):
                    specialopts = method[1]
                    optmethod = method[0]
                    #forward
                    com_name_forward = '{0}/{1}-{2}-{3}-tier{4}-forward.com'.format(reactants_dir,title,optmethod,basis_dict[optbasis],tier)
                    chk_name_forward = '{0}-{1}-{2}-tier{3}-forward.chk'.format(title,optmethod,basis_dict[optbasis],tier)
                    write_benchmarking_com(com_name_forward,chk_name_forward,optcores[tier],optmemory[tier],optmethod,optbasis,optroute_reactants,specialopts,charge,multiplicity,tier,basislist,title,'irc','forward')
                    #reverse
                    com_name_reverse = '{0}/{1}-{2}-{3}-tier{4}-reverse.com'.format(reactants_dir,title,optmethod,basis_dict[optbasis],tier)
                    chk_name_reverse = '{0}-{1}-{2}-tier{3}-reverse.chk'.format(title,optmethod,basis_dict[optbasis],tier)
                    write_benchmarking_com(com_name_reverse,chk_name_reverse,optcores[tier],optmemory[tier],optmethod,optbasis,optroute_reactants,specialopts,charge,multiplicity,tier,basislist,title,'irc','reverse')

                    with open('{0}/{1}-tier{2}.txt'.format(reactants_dir,title,tier),'a') as coms:
                        coms.write('{0}-{1}-{2}-tier{3}-forward.com\n'.format(title,optmethod,basis_dict[optbasis],tier))
                        coms.write('{0}-{1}-{2}-tier{3}-reverse.com\n'.format(title,optmethod,basis_dict[optbasis],tier))


    def _reactants_input(reactants_dir,title,optcores,optmemory,optmethod,optbasis,optroute_reactants,specialopts,charge,multiplicity):
        '''Write the input for just the lowest_ts IRC'''

        if os.path.exists('{0}/{1}.txt'.format(reactants_dir,title)):
            os.remove('{0}/{1}.txt'.format(reactants_dir,title))

        #forward
        com_name_forward = '{0}/{1}-forward.com'.format(reactants_dir,title)
        chk_name_forward = '{0}-forward.chk'.format(title)
        write_com(com_name_forward,chk_name_forward,optcores,optmemory,optmethod,optbasis,optroute_reactants,specialopts,charge,multiplicity)

        #reverse
        com_name_reverse = '{0}/{1}-reverse.com'.format(reactants_dir,title)
        chk_name_reverse = '{0}-reverse.chk'.format(title)
        write_com(com_name_reverse,chk_name_reverse,optcores,optmemory,optmethod,optbasis,optroute_reactants,specialopts,charge,multiplicity)

        with open('{0}/{1}-coms.txt'.format(reactants_dir,title),'a') as coms:
            coms.write('{0}-reverse.com\n'.format(title))
            coms.write('{0}-forward.com\n'.format(title))


    def _reactants_benchmarking_sbatch_template(tmptitle,tier,optpartition,optcores,optmemory,opttime,ncalcs,reactants_dir,title,g16root):
        '''write sbatch to submit tier of reactant calcs'''
    
        sbatch="""#!/bin/bash
#SBATCH --job-name={0}-tier{1}-REACTS
#SBATCH --output={7}/out.o
#SBATCH --error={7}/out.e
#SBATCH --partition={2}
#SBATCH --nodes=1
#SBATCH --ntasks={3}
#SBATCH --mem={4}G
#SBATCH --time={5}
#SBATCH --array=1-{6}%50
hostname
work={7}
cd $work

if [[ $SLURM_ARRAY_TASK_ID == 1 ]]
    then
    time=$(date)
    echo "$SLURM_JOB_NAME $time" >> ../status.txt

    #Submit failure
    ID=$SLURM_ARRAY_JOB_ID
    sbatch --dependency=afternotok:$ID {8}-tier{1}-failed.sbatch
    
else
    sleep 120s
fi

input=$(sed "${{SLURM_ARRAY_TASK_ID}}q;d" {8}-tier{1}.txt)
export INPUT=$input
export WORKDIR=$work
export GAUSS_SCRDIR=$work
export g16root={9}
. $g16root/g16/bsd/g16.profile
cd $WORKDIR
$g16root/g16/g16 $INPUT

station=$(grep "Station" -c ${{INPUT%.*}}.log)
if [[ $station -lt 2 ]]
    then
    exit 1234
fi

freq=$(tac ${{INPUT%.*}}.log | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
if [[ $freq -gt 0 ]]
    then 
    exit 1234
fi

""".format(tmptitle,tier,optpartition,optcores,optmemory,opttime,ncalcs*2,reactants_dir,title,g16root)
        return(sbatch)


    def _reactants_benchmarking_sbatch(benchmarkbasis,tmptitle,optpartition,optcores,optmemory,opttime,reactants_dir,title,g16root):
        '''write the template sbatch for each tier'''

        length_of_tiers = [len(basislist) for basislist in benchmarkbasis]
        max_tier = np.amax(length_of_tiers) 
    
        for tier in range(0,max_tier):
            nbasis = 0
            for tierlength in length_of_tiers:
                if tier < tierlength:
                    nbasis +=1
            ncalcs = nbasis * len(benchmarkmethods)
            with open('{0}/{1}-tier{2}.sbatch'.format(reactants_dir,title,tier),'w') as batch:
                batch.write(IRC._reactants_benchmarking_sbatch_template(tmptitle,tier,optpartition,optcores[tier],optmemory[tier],opttime,ncalcs,reactants_dir,title,g16root))
 
   
    def _reactants_sbatch(tmptitle,optpartition,optcores,optmemory,opttime,reactants_dir,title,g16root):
        '''write sbatch to submit tier of IRC calcs'''
    
        sbatch="""#!/bin/bash
#SBATCH --job-name={0}-REACTS
#SBATCH --output={5}/out.o
#SBATCH --error={5}/out.e
#SBATCH --partition={1}
#SBATCH --nodes=1
#SBATCH --ntasks={2}
#SBATCH --mem={3}G
#SBATCH --time={4}
#SBATCH --array=1-2

hostname
work={5}
cd $work
if [[ $SLURM_ARRAY_TASK_ID == 1 ]]
    then

    time=$(date)
    echo "$SLURM_JOB_NAME $time" >> ../status.txt

    #Submit failed
    ID=$SLURM_ARRAY_JOB_ID
    sbatch --dependency=afternotok:$ID {6}-failed.sbatch
    
    #get geometries
    for i in {6}-forward.com {6}-reverse.com
        do
        obabel ../irc/${{i%.*}}.log -o xyz | tail -n +3 >> $i
        echo " " >> $i
     done
 
else
    sleep 120s
fi

input=$(sed "${{SLURM_ARRAY_TASK_ID}}q;d" {6}-coms.txt)
export INPUT=$input
export WORKDIR=$work
export GAUSS_SCRDIR=$work
export g16root={7}
. $g16root/g16/bsd/g16.profile
cd $WORKDIR
$g16root/g16/g16 $INPUT

station=$(grep "Station" -c ${{INPUT%.*}}.log)
if [[ $station -lt 2 ]]
    then
    exit 1234
fi

freq=$(tac ${{INPUT%.*}}.log | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
if [[ $freq -gt 0 ]]
    then 
    exit 1234
fi


""".format(tmptitle,optpartition,optcores,optmemory,opttime,reactants_dir,title,g16root)
        with open('{0}/{1}-submit.sbatch'.format(reactants_dir,title), 'w') as batch:
            batch.write(sbatch)

    def _reactants_benchmarking_failed_template(tmptitle,short_partition,reactants_dir,title,tier,charge,multiplicity,errorlog):
        'template failure for reactants benchmarking'''

        sbatch=r"""#!/bin/bash
#SBATCH --job-name={0}-tier{4}-REACT-failed
#SBATCH --output={2}/resubmit.o
#SBATCH --error={2}/resubmit.e
#SBATCH --partition={1}
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --time=00:20:00
hostname

work={2}
cd $work
touch failed-script-ran
time=$(date)
echo "$SLURM_JOB_NAME $time" >> ../status.txt
if test -f {3}-tier{4}-resubmit.txt
    then
    nresub=$(sed "1q;d" {3}-tier{4}-resubmit.txt)
else
    nresub=0
fi
nresub=$((nresub+=1))
if [[ $nresub -lt 3 ]]
    then
    rm {3}-tier{4}-resubmit.txt
    echo $nresub >> {3}-tier{4}-resubmit.txt
    for i in {3}-*-tier{4}.log
        do
        echo "READING FILE $i" >>{3}-tier{4}-resublog.txt
        finished=$(grep 'Station' -c $i)
        freq=$(tac $i | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
        scf=$(grep "SCF Error SCF Error SCF Error SCF Error" $i -c )
        if [[ $finished -lt 2 ]]
            then
            convert=$(obabel $i -o xyz)
            if [[ $convert == *"0 molecules converted"* ]]
                then
                echo "${{i%.*}} did not reach restart point, or failed terribly" >> {3}-tier{4}-resublog.txt
                old=$(grep "%oldchk=" -c ${{i%.*}}.com)
                sed -i '1,/{5} {6}/!d' ${{i%.*}}.com
                echo " " >> ${{i%.*}}.com
                if [[ $old -gt 0 ]]
                    then
                    sed -i 1d ${{i%.*}}.com
                fi
                sed -i 's/geom=check//g' ${{i%.*}}.com
                sed -i 's/guess=read//g' ${{i%.*}}.com
                sed -i 's/opt=(readfc,maxstep=10)/opt/g' ${{i%.*}}.com
                sed -i 's/opt=(calcfc,maxstep=10)/opt/g' ${{i%.*}}.com
                sed -i 's/,maxstep=10//g' ${{i%.*}}.com
                sed -i 's/opt/opt=(calcfc,maxstep=10)/g' ${{i%.*}}.com 
                obabel ../irc/$i -o xyz | tail -n +3  >> ${{i%.*}}.com 
                echo " " >>  ${{i%.*}}.com
                echo '--Link1--' >>  ${{i%.*}}.com
                top=$(head -n 8 ${{i%.*}}.com)
                echo -ne "${{top/opt=(calcfc,maxstep=10)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                echo " " >>  ${{i%.*}}.com

            #SCF Convergence issues
            elif [[ $scf -gt 0 ]]
                then
                echo "${{i%.*}} SCF failed to converge, using scf=qc" >> {3}-tier{4}-resublog.txt
                sed -i 's/opt/scf=qc opt/g' ${{i%.*}}.com
            else

            sed -i '1,/{5} {6}/!d' ${{i%.*}}.com
            termination=$(grep "Normal termination" -c $i)
            cycles=$(grep "SCF Done" -c $i)
            check=$(grep "geom=check guess=read" -c ${{i%.*}}.com)
            
            old=$(grep "%oldchk=" -c ${{i%.*}}.com)

            #Non stationary point found
                 #read in fc
            if [[ $finished -eq 1 ]] && [[ $termination -ge 2 ]]
                then
                echo "${{i%.*}} finished with non-stationary point, reading previous fc" >> {3}-tier{4}-resublog.txt
                echo " " ${{i%.*}}.com
                if [[ $old -gt 0 ]]
                    then
                    sed -i 1d ${{i%.*}}.com
                fi
                sed -i 's/geom=check//g' ${{i%.*}}.com
                sed -i 's/guess=read//g' ${{i%.*}}.com
                sed -i 's/,maxstep=10//g' ${{i%.*}}.com
                sed -i 's/opt=(calcfc)/opt/g' ${{i%.*}}.com
                sed -i 's/opt=(readfc)/opt/g' ${{i%.*}}.com
                mv ${{i%.*}}.chk ${{i%.*}}-readingfc.chk
                echo " " >>  ${{i%.*}}.com
                echo '--Link1--' >>  ${{i%.*}}.com
                sed -i 's/opt/opt=(readfc,maxstep=10)/g' ${{i%.*}}.com
                top=$(head -n 8 ${{i%.*}}.com)
                echo -ne "${{top/opt=(readfc,maxstep=10)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                sed -i 's/opt=(readfc,maxstep=10)/opt=(readfc,maxstep=10) geom=check guess=read/g' ${{i%.*}}.com
                sed -i "1s/^/%oldchk=${{i%.*}}-readingfc.chk\n/" ${{i%.*}}.com
                echo " " >>${{i%.*}}.com
 
             #stationary found, but didnt finish frequencies or far from starting geometry
                 #re-calculate force constants
             elif ([[ $finished -eq 1 ]] && [[ $termination -lt 2 ]]) || ([[ $cycles -gt 15 ]])
                then
                echo "${{i%.*}} didnt finish freq, or is far from starting geometry" >> {3}-tier{4}-resublog.txt
                if [[ $old -gt 0 ]]
                    then
                    sed -i 1d ${{i%.*}}.com
                fi
                obabel $i -o xyz | tail -n +3 >> ${{i%.*}}.com
                sed -i 's/,maxstep=10//g' ${{i%.*}}.com
                sed -i 's/geom=check//g' ${{i%.*}}.com
                sed -i 's/guess=read//g' ${{i%.*}}.com
                sed -i 's/opt=(calcfc)/opt/g' ${{i%.*}}.com
                sed -i 's/opt=(readfc)/opt/g' ${{i%.*}}.com
                sed -i 's/opt/opt=(calcfc,maxstep=10)/g' ${{i%.*}}.com
                echo " " >> ${{i%.*}}.com
                echo '--Link1--' >>  ${{i%.*}}.com
                top=$(head -n 8 ${{i%.*}}.com)
                echo -ne "${{top/opt=(calcfc,maxstep=10)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                echo " " >>${{i%.*}}.com

             #no stationary point found yet
             else
                
                fc=$(grep "Converged?" -c $i)
  
                #if force constants were finished computing, read them
                if [[ $fc -gt 0 ]]
                    then
                    echo "${{i%.*}} no stationary point found, reading fc" >> {3}-tier{4}-resublog.txt
                    if [[ $old -gt 0 ]]
                        then
                        sed -i 1d ${{i%.*}}.com
                    fi
                    sed -i 's/geom=check//g' ${{i%.*}}.com
                    sed -i 's/guess=read//g' ${{i%.*}}.com
                    sed -i 's/,maxstep=10//g' ${{i%.*}}.com
                    sed -i 's/opt=(calcfc)/opt/g' ${{i%.*}}.com
                    sed -i 's/opt=(readfc)/opt/g' ${{i%.*}}.com
                    mv ${{i%.*}}.chk ${{i%.*}}-readingfc.chk
                    sed -i 's/opt/opt=(readfc,maxstep=10)/g' ${{i%.*}}.com
                    echo " " >> ${{i%.*}}.com
                    echo '--Link1--' >>  ${{i%.*}}.com
                    top=$(head -n 8 ${{i%.*}}.com)
                    echo -ne "${{top/opt=(readfc,maxstep=10)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                    sed -i 's/opt=(readfc,maxstep=10)/opt=(readfc,maxstep=10) geom=check guess=read/g' ${{i%.*}}.com
                    sed -i "1s/^/%oldchk=${{i%.*}}-readingfc.chk\n/" ${{i%.*}}.com
                    echo " " >>${{i%.*}}.com 

                 #if not, take geometry and restart
                 else
                    echo "${{i%.*}} no stationary point found, nor fc, starting again" >> {3}-tier{4}-resublog.txt
                    obabel $i -o xyz |tail -n +3 >> ${{i%.*}}.com
                    if [[ $old -gt 0 ]]
                        then
                        sed -i 1d ${{i%.*}}.com
                    fi
                    sed -i 's/geom=check//g' ${{i%.*}}.com
                    sed -i 's/guess=read//g' ${{i%.*}}.com
                    sed -i 's/,maxstep=10//g' ${{i%.*}}.com
                    sed -i 's/opt=(calcfc)/opt/g' ${{i%.*}}.com
                    sed -i 's/opt=(readfc)/opt/g' ${{i%.*}}.com
                    sed -i 's/opt/opt=(calcfc,maxstep=10)/g' ${{i%.*}}.com 
                    echo " " >>${{i%.*}}.com
                    echo '--Link1--' >>  ${{i%.*}}.com
                    top=$(head -n 8 ${{i%.*}}.com)
                    echo -ne "${{top/opt=(calcfc,maxstep=10)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                    echo " " >>${{i%.*}}.com

                fi
            fi
            fi
        echo ${{i%.*}}.com >> {3}-tier{4}-resubmit.txt
    echo " " >> ${{i%.*}}.com

    elif [[ $finished -gt 1 ]] && [[ $freq -gt 0 ]]
        then
             #stationary found, but its a saddle point
                 #re-calculate force constants
            echo "${{i%.*}} Saddle point found" >> {3}-tier{4}-resublog.txt
            old=$(grep "%oldchk=" -c ${{i%.*}}.com)
            sed -i '1,/{5} {6}/!d' ${{i%.*}}.com
            if [[ $old -gt 0 ]]
                then
                sed -i 1d ${{i%.*}}.com
            fi
                obabel $i -o xyz | tail -n +3 >> ${{i%.*}}.com
                sed -i 's/,maxstep=10//g' ${{i%.*}}.com
                sed -i 's/geom=check//g' ${{i%.*}}.com
                sed -i 's/guess=read//g' ${{i%.*}}.com
                sed -i 's/opt=(calcfc)/opt/g' ${{i%.*}}.com
                sed -i 's/opt=(readfc)/opt/g' ${{i%.*}}.com
                sed -i 's/opt/opt=(calcfc,maxstep=10)/g' ${{i%.*}}.com
                echo " " >> ${{i%.*}}.com
                echo '--Link1--' >>  ${{i%.*}}.com
                top=$(head -n 8 ${{i%.*}}.com)
                echo -ne "${{top/opt=(calcfc,maxstep=10)/freq=noraman geom=check guess=read}}" >> ${{i%.*}}.com
                echo ${{i%.*}}.com >> {3}-tier{4}-resubmit.txt
                echo " " >> ${{i%.*}}.com

    else
        echo "$i is done" >> {3}-tier{4}-resublog.txt
    fi
    
    done
    toresub=$(cat {3}-tier{4}-resubmit.txt |wc -l)
    sed -i "s/#SBATCH --array=.*/#SBATCH --array=2-$toresub/g" {3}-tier{4}.sbatch
    sed -i "s/{3}-tier{4}.txt/{3}-tier{4}-resubmit.txt/g" {3}-tier{4}.sbatch
    ID=$(sbatch --parsable {3}-tier{4}.sbatch)
    sbatch --dependency=afternotok:$ID {3}-tier{4}-failed.sbatch

else
    if test -f {3}-tier{4}-NEEDS_MANUAL_FIX.txt
        then
        rm {3}-tier{4}-NEEDS_MANUAL_FIX.txt
    fi
    echo 'Falied too many times and need manual attention - re-submit with {3}-tier{4}.sbatch after making changes' >> {3}-tier{4}-NEEDS_MANUAL_FIX.txt
    for i in {3}-*-tier{4}.log
        do
        finished=$(grep 'Station' -c $i)
        if [[ $finished -lt 2 ]]
            then
            echo ${{i%.*}}.com >> {3}-tier{4}-NEEDS_MANUAL_FIX.txt
        else
            freq=$(tac $i | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
            if [[ $freq -gt 0 ]]
                then 
                echo ${{i%.*}}.com >> {3}-tier{4}-NEEDS_MANUAL_FIX.txt
            fi
        fi
    done
    toresub=$(cat {3}-tier{4}-NEEDS_MANUAL_FIX.txt |wc -l)
    sed -i "s/#SBATCH --array=.*/#SBATCH --array=2-$toresub/g" {3}-tier{4}.sbatch
    sed -i "s/{3}-tier{4}-resubmit.txt/{3}-tier{4}-NEEDS_MANUAL_FIX.txt/g" {3}-tier{4}.sbatch
    echo "{3} failed too many times. RUN TERMINATED" >> ../status.txt
    echo "{3} failed too many times. RUN TERMINATED" >> {7}/{3}
fi


""".format(tmptitle,short_partition,reactants_dir,title,tier,charge,multiplicity,errorlog)
        return(sbatch)

    def _reactants_benchmarking_failed(benchmarkbasis,tmptitle,short_partition,reactants_dir,title,charge,multiplicity,errorlog):
        '''write the template sbatch for each tier'''

        length_of_tiers = [len(basislist) for basislist in benchmarkbasis]
        max_tier = np.amax(length_of_tiers) 
    
        for tier in range(0,max_tier):
            with open('{0}/{1}-tier{2}-failed.sbatch'.format(reactants_dir,title,tier),'w') as batch:
                batch.write(IRC._reactants_benchmarking_failed_template(tmptitle,short_partition,reactants_dir,title,tier,charge,multiplicity,errorlog))
  
    def _reactants_failed(tmptitle,short_partition,reactants_dir,title,charge,multiplicity,errorlog):
        'template failure for reactants benchmarking'''

        sbatch=r"""#!/bin/bash
#SBATCH --job-name={0}-REACTS-failed
#SBATCH --output={2}/resubmit.o
#SBATCH --error={2}/resubmit.e
#SBATCH --partition={1}
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --time=00:20:00
hostname

work={2}
cd $work
touch failed-script-ran
time=$(date)
echo "$SLURM_JOB_NAME $time" >> ../status.txt
if test -f {3}-resubmit.txt
    then
    nresub=$(sed "1q;d" {3}-resubmit.txt)
else
    nresub=0
fi
nresub=$((nresub+=1))
if [[ $nresub -lt 3 ]]
    then
    rm {3}-resubmit.txt
    echo $nresub >> {3}-resubmit.txt
    for i in {3}-forward.log {3}-reverse.log
        do
        finished=$(grep 'Station' -c $i)
        freq=$(tac $i | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
            if [[ $finished -lt 2 ]]
            then
            convert=$(obabel $i -o xyz)
            if [[ $convert == *"0 molecules converted"* ]]
                then
                echo "${{i%.*}} could not be converted, reverting to original" >> {3}-tier{4}-resublog.txt
                old=$(grep "%oldchk=" -c ${{i%.*}}.com)
                sed -i '1,/{4} {5}/!d' ${{i%.*}}.com
                echo " " ${{i%.*}}.com
                if [[ $old -gt 0 ]]
                    then
                    sed -i 1d ${{i%.*}}.com
                fi
                sed -i 's/geom=check//g' ${{i%.*}}.com
                sed -i 's/guess=read//g' ${{i%.*}}.com
                sed -i 's/opt=readfc/opt=calcfc/g' ${{i%.*}}.com
                sed -i 's/opt /opt=calcfc /g' ${{i%.*}}.com
                obabel ../irc/ $i -o xyz | tail -n +3 >> ${{i%.*}}.com
                echo " " >>  ${{i%.*}}.com
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
                echo "${{i%.*}} Non-stationary point found, reading previous fc" >> {3}-resublog.txt
                echo " " >> ${{i%.*}}.com
                if [[ $old -gt 0 ]]
                    then
                    sed -i 1d ${{i%.*}}.com
                fi
                sed -i 's/geom=check//g' ${{i%.*}}.com
                sed -i 's/guess=read//g' ${{i%.*}}.com
                mv ${{i%.*}}.chk ${{i%.*}}-readingfc.chk
                sed -i 's/opt /opt=readfc /g' ${{i%.*}}.com
                sed -i 's/opt=calcfc/opt=readfc/g' ${{i%.*}}.com
                sed -i 's/opt=readfc/opt=readfc geom=check guess=read/g' ${{i%.*}}.com
                sed -i "1s/^/%oldchk=${{i%.*}}-readingfc.chk\n/" ${{i%.*}}.com
                echo " " >> ${{i%.*}}.com

             #stationary found, but didnt finish frequencies or far from starting geometry
                 #re-calculate force constants
             elif ([[ $finished -eq 1 ]] && [[ $termination -lt 2 ]]) || ([[ $cycles -gt 15 ]])
                then
                echo "${{i%.*}} failed frequencies or is far from input geometry" >> {0}-resublog.txt
                if [[ $old -gt 0 ]]
                    then
                    sed -i 1d ${{i%.*}}.com
                fi
                obabel $i -o xyz | tail -n +3 >> ${{i%.*}}.com
                echo " " >> ${{i%.*}}.com
                sed -i 's/geom=check//g' ${{i%.*}}.com
                sed -i 's/guess=read//g' ${{i%.*}}.com
                sed -i 's/opt /opt=calcfc /g' ${{i%.*}}.com
                sed -i 's/opt=readfc/opt=calcfc/g' ${{i%.*}}.com
                echo " " >> ${{i%.*}}.com

             #no stationary point found yet
             else
                fc=$(grep "Converged?" -c $i)
  
                #if force constants were finished computing, read them
                if [[ $fc -gt 0 ]]
                    then
                    echo "${{i%.*}} did not find stationary point, reading fc" >> {3}-resublog.txt
                    echo " " >> ${{i%.*}}.com
                    if [[ $old -gt 0 ]]
                        then
                        sed -i 1d ${{i%.*}}.com
                    fi
                    sed -i 's/geom=check//g' ${{i%.*}}.com
                    sed -i 's/guess=read//g' ${{i%.*}}.com
                    mv ${{i%.*}}.chk ${{i%.*}}-readingfc.chk
                    sed -i 's/opt=calcfc/opt=readfc/g' ${{i%.*}}.com
                    sed -i 's/opt /opt=readfc /g' ${{i%.*}}.com
                    sed -i 's/opt=readfc/opt=readfc geom=check guess=read/g' ${{i%.*}}.com
                    sed -i "1s/^/%oldchk=${{i%.*}}-readingfc.chk\n/" ${{i%.*}}.com
                    echo " " >> ${{i%.*}}.com
                 #if not, take geometry and restart
                 else
                    echo "${{i%.*}} did not find stationary point and has no fc" >> {3}-resublog.txt
                    obabel $i -o xyz |tail -n +3 >> ${{i%.*}}.com
                    echo " " >> ${{i%.*}}.com
                    if [[ $old -gt 0 ]]
                        then
                        sed -i 1d ${{i%.*}}.com
                    fi
                    sed -i 's/geom=check//g' ${{i%.*}}.com
                    sed -i 's/guess=read//g' ${{i%.*}}.com
                    sed -i 's/opt=readfc/opt=calcfc/g' ${{i%.*}}.com 
                    sed -i 's/opt /opt=calcfc /g' ${{i%.*}}.com
                    echo " " >> ${{i%.*}}.com
                fi
            fi
            fi
        echo ${{i%.*}}.com >> {3}-resubmit.txt
        echo " " >> ${{i%.*}}.com

    elif [[ $finished -gt 1 ]] && [[ $freq -gt 0 ]]
        then
             #stationary found, but its a saddle point
                 #re-calculate force constants
            echo "${{i%.*}} Saddle point found" >> {3}-resublog.txt
            old=$(grep "%oldchk=" -c ${{i%.*}}.com)
            sed -i '1,/{4} {5}/!d' ${{i%.*}}.com
            if [[ $old -gt 0 ]]
                then
                sed -i 1d ${{i%.*}}.com
            fi
            obabel $i -o xyz | tail -n +3 >> ${{i%.*}}.com
            echo " " >> ${{i%.*}}.com
            sed -i 's/geom=check//g' ${{i%.*}}.com
            sed -i 's/guess=read//g' ${{i%.*}}.com
            sed -i 's/opt /opt=calcfc /g' ${{i%.*}}.com
            sed -i 's/opt=readfc/opt=calcfc/g' ${{i%.*}}.com
            echo ${{i%.*}}.com >> {3}-resubmit.txt
            echo " " >> ${{i%.*}}.com
 
    fi
    done

    toresub=$(cat {3}-resubmit.txt |wc -l)
    sed -i "s/#SBATCH --array=.*/#SBATCH --array=2-$toresub/g" {3}-submit.sbatch
    sed -i "s/{3}-coms.txt/{3}-resubmit.txt/g" {3}-submit.sbatch
    ID=$(sbatch --parsable {3}-submit.sbatch)
    sbatch --dependency=afternotok:$ID {3}-failed.sbatch

else
    for i in {3}-forward.log {3}-reverse.log
        do
        finished=$(grep 'Station' -c $i)
        if [[ $finished -lt 2 ]]
            then
            echo ${{i%.*}}.com >> {3}-NEEDS_MANUAL_FIX.txt
         else
             freq=$(tac $i | grep "imaginary frequencies (negative Signs)"  -m1 |awk '{{ print $2 }}' )
             if [[ $freq -gt 0 ]]
                 then 
                 echo ${{i%.*}}.com >> {3}-NEEDS_MANUAL_FIX.txt
             fi
        fi
    done
    toresub=$(cat {3}-NEEDS_MANUAL_FIX.txt |wc -l)
    sed -i "s/#SBATCH --array=.*/#SBATCH --array=2-$toresub/g" {3}-submit.sbatch
    sed -i "s/{3}-tier{4}-resubmit.txt/{3}-NEEDS_MANUAL_FIX.txt/g" {3}-submit.sbatch
    echo "{3} failed too many times. RUN TERMINATED" >> ../status.txt
    echo "{3} failed too many times. RUN TERMINATED" >> {6}/{3}
fi


""".format(tmptitle,short_partition,reactants_dir,title,charge,multiplicity,errorlog)
        with open('{0}/{1}-failed.sbatch'.format(reactants_dir,title),'w') as batch:
            batch.write(sbatch)


########################
### Perform Setup ###
########################

def main():
    ## This is the main function

    #with open('rotation.out','w') as log:
        #log.write(header)
        
    parser = OptionParser()
    parser.add_option('-c', dest='input',    type=str,   nargs=1, help='Input coordinates file, xyz or log.')
    parser.add_option('-l', dest='list',     type=str,   nargs=1, help='List of input coordinates file, will override -c option')
    parser.add_option('-a', dest='axis',     type=str,   nargs=1, help='List of axis atoms, should be quoted. Default is search two closest N atoms',default='A1 N')
    parser.add_option('-b', dest='angles',   type=str,   nargs=1, help='List of rotation angles, should be quoted. Default is no rotation',default='')
    parser.add_option('--benchmark', dest='benchmark',  action="store_true", help='Generate DFT benchmarking input files',default=False)
    parser.add_option('--irc',dest='irc',action="store_true",help='preform IRC from final TS and optimize the lowest energy structre as reactant',default=False)


    (options, args) = parser.parse_args()
    input=options.input
    list=options.list
    axis=options.axis
    angles=options.angles
    benchmark=options.benchmark
    irc=options.irc
 

    return input,list,axis,angles,benchmark,irc

def gen_inputs(input,list,axis,angles,benchmark,irc,utilities_dir,ts_guess_dir,conf_search_dir,lowest_ts_dir,conf_opt_dir,input_dir,benchmark_dir,irc_dir,reactants_dir):

    #print(sys.path)
    header="""
-------------------------------------------------------

    EZ-TS:  Automatic Transition State Workflow
                         
                         Patrick Neal and Dan Adrion
                         feat. MoRot - Jingbai Li

-------------------------------------------------------
"""
    print(header)

    #setting up TS manipulation
    #Check for list of torions to move

    global frag1
    if list == None and input == None:
        print('\n!!! Unkown coordinate file !!!\n')
        print(usage)
        print('\n!!! Unkown coordinate file !!!\n')
        exit()

    axis=axis.upper().split()
    angles=angles.upper().split()
    opt_axis,opt_angles=ReadOpt(axis,angles)
    if list != None:
        jobs=Readlist(list,opt_axis,opt_angles)
    else:
        jobs=[[input,opt_axis,opt_angles,1]]


    #start processing each job (molecule with rotation instructions) in the file provided
    jobs_per_mol = 12 # one for each of the 12 guesses
    count = 1
    for n,i in enumerate(jobs):
        frag1=[]
        file,ax,ang,index=i
        
        #MoRot is the molecule rotator that does the heavy lifting of 
        #1 - reading the input structure
        #2 - manipulating the minima structre to 12 TS guess structures
        #3 - outputting information used to set up all of the calculations
        try:
            charge,multiplicity,c1,a1,a2,c2,title,xyz,new_mol,natom=MoRot(file,ax,ang,index,optcores,optmemory,optmethod,optbasis,ts_guessroute,ts_guess_dir,specialopts)
            rotation_successful = True
        except:
            print('Could not generate TS guess number {0} coordinates for {1}'.format(count,file))
            rotation_successful = False
            
        #for the first TS guess structure of each input molecule, setup all the scripts
        if rotation_successful:
            if count == 1:
                #shorten the title if its really long
                if len(title) > 20:
                    tmptitle=title[0:10]
                else:
                    tmptitle=title

                #ts_guess (actual input file written within MoRot)
                ts_guess._sbatch(tmptitle,optpartition,optcores[0],optmemory[0],opttime,jobs_per_mol,ts_guess_dir,title,runlog,g16root)
                ts_guess._failed(tmptitle,short_partition,ts_guess_dir,title,charge,multiplicity,conf_search_dir,ts_guessroute)
                with open('{0}/{1}-coms.txt'.format(ts_guess_dir,title),'w') as coms:
                    coms.write("{0}-rot-{1}.com\n".format(title,index))

                #conf search
                CRESTdir = '{0}/{1}/CREST'.format(conf_search_dir,title)
                ORCAdir = '{0}/{1}/ORCA'.format(conf_search_dir,title)
                conf_search._CREST_constraints(c1,c2,a1,a2,tmptitle,CRESTdir,title,natom)
                conf_search._CREST_sbatch(tmptitle,CRESTpartition,CRESTcores,CRESTmem,CRESTtime,ts_guess_dir,title,utilities_dir,XTBPATH,LD_LIBRARY_PATH,CRESTdir,CRESTmethod,c1,a1,a2,c2)
                conf_search._ORCA_input(ORCAmethod,ORCAcores,ORCAmem,title,c1,c2,a1,a2,ORCAdir,ORCAoptsteps,charge,multiplicity)
                conf_search._ORCA_sbatch(tmptitle,ORCAcores,ORCAtime,ORCApartition,ORCAmem,ORCAdir,ORCA_EXE,OPENMPI,title,ORCAmethod,errorlog)

                #conf opt
                conf_opt._inputs(conf_opt_dir,title,optcores[0],optmemory[0],optmethod,optbasis,optroute,specialopts,charge,multiplicity)
                conf_opt._sbatch(tmptitle,optpartition,optcores[0],optmemory[0],opttime,conf_opt_dir,title,charge,multiplicity,conf_search_dir,g16root)
                conf_opt._failed(tmptitle,short_partition,conf_opt_dir,title,charge,multiplicity,lowest_ts_dir,errorlog)

                #Lowest ts
                getlowest(title,conf_opt_dir,utilities_dir,benchmark,runlog,short_partition,tmptitle,irc,c1,a1,a2,c2,lowest_ts_dir)

                if benchmark:
                    #WRITE BENCHMARKING HERE
                    benchmarking._input(benchmarkmethods,benchmarkbasis,benchmark_dir,title,optmethod,optcores,optmemory,optbasis,optroute,charge,multiplicity)
                    benchmarking._sbatch(benchmarkbasis,tmptitle,optpartition,optcores,optmemory,opttime,benchmark_dir,title,g16root)
                    benchmarking._failed(tmptitle,short_partition,benchmark_dir,title,charge,multiplicity,errorlog,benchmarkbasis)

                if irc:
                    #WRITE IRC HERE
                    if benchmark:
                        IRC._benchmarking_input(benchmarkmethods,benchmarkbasis,irc_dir,optcores,optmemory,ircroute_forward,ircroute_reverse,charge,multiplicity,title)
                        IRC._benchmarking_sbatch(benchmarkbasis,tmptitle,optpartition,optcores,optmemory,opttime,irc_dir,title,g16root)
                        IRC._benchmarking_reactants_input(benchmarkmethods,benchmarkbasis,reactants_dir,optcores,optmemory,optroute_reactants,charge,multiplicity,title)
                        IRC._reactants_benchmarking_sbatch(benchmarkbasis,tmptitle,optpartition,optcores,optmemory,opttime,reactants_dir,title,g16root)
                        IRC._reactants_benchmarking_failed(benchmarkbasis,tmptitle,short_partition,reactants_dir,title,charge,multiplicity,errorlog)
                    else:
                        IRC._input(irc_dir,title,optcores[0],optmemory[0],optmethod,optbasis,ircroute_forward,ircroute_reverse,specialopts,charge,multiplicity)
                        IRC._sbatch(tmptitle,optpartition,optcores[0],optmemory[0],opttime,irc_dir,title,g16root)
                        IRC._reactants_input(reactants_dir,title,optcores[0],optmemory[0],optmethod,optbasis,optroute_reactants,specialopts,charge,multiplicity)
                        IRC._reactants_sbatch(tmptitle,optpartition,optcores[0],optmemory[0],opttime,reactants_dir,title,g16root)
                        IRC._reactants_failed(tmptitle,short_partition,reactants_dir,title,charge,multiplicity,errorlog)

            #If not the first in the molecule batch, just add the name to the list of TS guesses
            else:
                #list of input files for ts_guess
                with open('{0}/{1}-coms.txt'.format(ts_guess_dir,title),'a') as coms:
                    coms.write("{0}-rot-{1}.com\n".format(title,index))

        #if the count is less than the jobs per molecule, it is the same molecule, so grab the next
        if count < jobs_per_mol:
            count+=1
        #if the count is greater than the jobs per molecule, then all guesses were processed for the molecule, reset count for the next
        else:
            count=1

        sys.stdout.write('Progress: %10s/%s\r' % (n+1,len(jobs)))

    print('')



if __name__ == '__main__':
    input,list,axis,angles,benchmark,irc = main()
    gen_inputs(input,list,axis,angles,benchmark,irc,utilities_dir,ts_guess_dir,conf_search_dir,lowest_ts_dir,conf_opt_dir,input_dir,benchmark_dir,irc_dir,reactants_dir)


