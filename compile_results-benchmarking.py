import pandas as pd
import itertools
import json
import argparse
import numpy as np
import re
from os.path import join
from datetime import datetime
import glob
import os
import sys
import shutil
from numpy import linalg as la

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


def Read_azo(filename):
    for line in open(filename,'r'):
        if re.search('python3 ../utilities/get_lowest.py',line):
            c1 = int(line.split()[3])
            a1 = int(line.split()[4])
            a2 = int(line.split()[5])
            c2 = int(line.split()[6])
    return(c1,a1,a2,c2)

def ReadG16(title):
    ''' Read a log file '''

    with open(title,'r') as logfile:
        log=logfile.read().splitlines()

    natom=0
    coord=[]
    xyz=[]
    atoms=[]
    for n,line in enumerate(log):
        if 'NAtoms' in line:
            natom=int(line.split()[1])

    for n,line in enumerate(log):
        if 'Standard orientation' in line:
            coord=log[n+5:n+5+natom]

    for line in coord:
        c,e,t,x,y,z=line.split()
        n=Element(e).getNuc()
        x,y,z=float(x),float(y),float(z)
        atoms.append(n)
        xyz.append([x,y,z])

    xyz=np.array(xyz)
    return natom,atoms,xyz

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

methods_dict={
    "M11L":"M11-L",
    "SVWN":"SVWN",
    "SVWN5":"SVWN5",
    "MN12SX":"MN12-SX",
    "M062X":"M06-2X",
    "M06HF":"M06-HF",
    "N12SX":"N12-SX",
    "MPWb95":"MPW1B95",
    "PBE1PBE":"PBE0-D3BJ",
    "PBEh1PBE":"PBEh1PBE",
    "OHSE2PBE":"OSHE2PBE",
    "mPW1PBE":"MPW1PBE",
    "mPW1PW91":"MPW1PW91",
    "APFD":"APFD",
    "TPSSH":"TPSSH",
    "B3P86":"B3P86",
    "tpsskcis":"TPSS1KCIS",
    "B3LYP":"B3LYP-D3BJ",
    "BHandH":"BHandH",
    "BMK":"BMK-D3BJ",
    "MPWB95":"MPWB1k",
    "MPWPW91":"MPW1K",
    "bb95":"BB1K",
    "wb97xd":"wB97X-D",
    "wb97":"wB97",
    "wb97x":"wB97X",
    "cam-b3lyp":"cam-B3LYP-D3BJ",
    "LC-wHPBE":"LC-wHPBE"
    }

methods_dict_list = ["M11L","SVWN","SVWN5","MN12SX","M062X","M06HF","N12SX","MPWb95","PBE1PBE","PBEh1PBE","OHSE2PBE","mPW1PBE","mPW1PW91","APFD","TPSSH","B3P86","tpsskcis","B3LYP","BHandH","BMK","MPWB95","MPWPW91","bb95","wb97xd","wb97","wb97x","cam-b3lyp","LC-wHPBE"]

basis_dict={
    "pople":"6-31G(d)",
    "pople-plusdp":"6-31+G(d,p)",
    "pople-tz":"6-311+G(d,p)",
    "cc-pvdz":"cc-pvdz",
    "cc-pvtz":"cc-pvtz",
    "aug-cc-pvdz":"aug-cc-pvdz",
    "aug-cc-pvtz":"aug-cc-pvtz"
    }

basis_dict_list = ["pople","pople-plusdp","pople-tz","cc-pvdz","cc-pvtz","aug-cc-pvdz","aug-cc-pvtz"]


##########################################################################################################################################

def verify_finished(filename,type):
    if type == 'reactant':
        freqthresh = 1
        #no match to 'imaginary frequencies' if reactant is complete
        freq = 0
    elif type == 'ts':
        freqthresh = 2
        #ensure that 1 imaginary frequencies was found - ie don't allow pass frequency if none present
        freq = 10

    station = 0
    #regex is not working for the 'imaginary frequencies' string, look for whole line match instead
    for line in open(filename,'r'):
        if re.search('Stationary',line):
            station+=1
        #elif re.search('1 imaginary frequencies (negative Signs)',line):
        elif line.strip() == '******    1 imaginary frequencies (negative Signs) ******':
            freq = 1
        #elif re.search('2 imaginary frequencies (negative Signs)',line):
        elif line.strip() == '******    2 imaginary frequencies (negative Signs) ******':
            freq = 2
        elif line.strip() == '******    3 imaginary frequencies (negative Signs) ******':
            freq = 3


    if station > 1 and freq < freqthresh:
        #print('valid',station,freq,filename)
        return(True)
    else:
        #print('not valid',station,freq,filename)
        return(False)
  

def get_cis(barriers,input):

    #forward reactant energies
    forward = pd.DataFrame().reindex_like(barriers)
    cols = forward.columns
    for mol,row in forward.iterrows():
        for col in cols:
            filename = '{2}/reactants/{0}-{1}-forward.log'.format(mol,col,input)
            if os.path.exists(filename):
                if verify_finished(filename,'reactant'):
                    for line in open(filename,'r'):
                        if re.search('Sum of electronic and thermal Free Energies',line):
                            energy = line.split('=')[-1].strip()
                            forward.at[mol,col] = energy
           

    #reverse reactant energies
    reverse = pd.DataFrame().reindex_like(barriers)
    cols = reverse.columns
    for mol,row in reverse.iterrows():
        for col in cols:
            filename = '{2}/reactants/{0}-{1}-reverse.log'.format(mol,col,input)
            if os.path.exists(filename):
                if verify_finished(filename,'reactant'):
                    for line in open(filename,'r'):
                        if re.search('Sum of electronic and thermal Free Energies',line):
                            energy = line.split('=')[-1].strip()
                            reverse.at[mol,col] = energy

    #figure out which is lower in energy
    higher_energy = pd.DataFrame().reindex_like(barriers).astype('object')
    cols = higher_energy.columns
    for mol,row in higher_energy.iterrows():
        for x,col in enumerate(cols):
            difference = (forward[col][mol] - reverse[col][mol])*627.509
            if np.absolute(difference) < 2. :
                lowest = 'Close in energy'
        #ME
            elif difference > 0.:
                cis = forward[col][mol]
                shutil.copy('{2}/reactants/{0}-{1}-reverse.log'.format(mol,col,input),'{0}/trans/{1}-{2}-reverse.log'.format(input,mol,col))
                shutil.copy('{2}/reactants/{0}-{1}-forward.log'.format(mol,col,input),'{0}/cis/{1}-{2}-forward.log'.format(input,mol,col))
            elif difference < 0. :
                cis = reverse[col][mol]
                shutil.copy('{2}/reactants/{0}-{1}-forward.log'.format(mol,col,input),'{0}/trans/{1}-{2}-forward.log'.format(input,mol,col))
                shutil.copy('{2}/reactants/{0}-{1}-reverse.log'.format(mol,col,input),'{0}/cis/{1}-{2}-reverse.log'.format(input,mol,col))
            else:
                cis = 'NaN'

            higher_energy.at[mol,col] = cis

    return(higher_energy)

def get_ts(barriers,input):
    ts = pd.DataFrame().reindex_like(barriers).astype('object')
    freqs = pd.DataFrame().reindex_like(barriers)
    times = pd.DataFrame().reindex_like(barriers)
    max_angles = pd.DataFrame().reindex_like(barriers)

    cols = ts.columns

    for mol,row in ts.iterrows():
        c1,a1,a2,c2 = Read_azo('{0}/lowest_ts/{1}-lowest.sbatch'.format(input,mol))
        for col in cols:
            filename = '{2}/benchmarking/{0}-{1}.log'.format(mol,col,input)
            if os.path.exists(filename):
                if verify_finished(filename,'ts'):
                    natom,atoms,xyz = ReadG16(filename)
                    Ang1 = Ang(xyz,c1,a1,a2)
                    Ang2 = Ang(xyz,c2,a2,a1)   
                    Angs = [Ang1,Ang2]
                    max_angle = np.amax(Angs)
                    max_angles.at[mol,col] = max_angle
                    for line in open(filename,'r'):
                        if re.search('Sum of electronic and thermal Free Energies',line):
                            energy = line.split('=')[-1].strip()
                            #if max_angle < 140.:
                            #    ts.at[mol,col]='Check TS - small max_angle'
                            #else:
                            ts.at[mol,col] = energy
                        elif re.search('Frequencies --   -',line):
                            freq = line.split()[2]
                            freqs.at[mol,col] = freq
                        elif re.search('Job cpu time:',line):
                            days = float(line.split()[3])
                            hours = float(line.split()[5])
                            minutes = float(line.split()[7])
                            seconds = float(line.split()[9])
                            time = (days * 24 * 60) + (hours * 60) + minutes + (seconds/60.)
                            times.at[mol,col] = time
                   
    return(ts,freqs,times,max_angles)
 
def get_barriers(barriers,ts,cis,input):

    cols = barriers.columns
    missing = 0
    for mol,row in barriers.iterrows():
        for x,col in enumerate(cols):
            if cis[col][mol] == 'Close in energy':
                barriers.at[mol,col]='Check TS - reactants are equal energy'
            #elif ts[col][mol] == 'Check TS - small max_angle':
                #barriers.at[mol,col]='Check TS - small max_angle'
            elif np.isnan(float(ts[col][mol])) and np.isnan(float(cis[col][mol])):
                barriers.at[mol,col] = 'Missing Both'
                missing += 1
            elif np.isnan(float(ts[col][mol])):
                barriers.at[mol,col] = 'Missing TS'
                missing += 1
            elif np.isnan(float(cis[col][mol])):
                barriers.at[mol,col] = 'Missing cis'
                missing += 1
            else:
                barrier = (float(ts[col][mol]) - float(cis[col][mol]))*627.509
                barriers.at[mol,col] = barrier

    total = barriers.shape[0] * barriers.shape[1]
    completed = total - missing
    print('{0} barriers from {1} processed, {2} barriers complete ({3:.1f}%)'.format(total,input,completed,(completed/total)*100))
    return(barriers)


##########################################################################################################################################
def ME(datas,indices,known_barriers):
    differences = [ (known_barriers[indices[index]] - data) for index,data in enumerate(datas) ]  
    return(np.mean(differences))

def MAE(datas,indices,known_barriers):
    differences = [ np.absolute(known_barriers[indices[index]] - data) for index,data in enumerate(datas) ]
    return(np.mean(differences))

def count_inversion(datas):
    return(list(datas).count(True))

def count_rotation(datas):
    return(list(datas).count(False))

#############################################################################################################################################

def main():

    parser = argparse.ArgumentParser(description='Compile data')
    parser.add_argument('--directories','-d', dest='inputs', help='EZ-TS directories to compile data from - if none specified, assumes its being run from the utilities directory of an EZ-TS run',nargs='*',default=None)
    parser.add_argument('--experimental','-e',dest='known_barriers',help=r'This should be an escaped json string of molecule:barrier key:value pars like "{\"mol1\":15,\"mol1\":22}" including quotes',default=None,type=str,nargs=1)

    parser.add_argument('--output','-o',dest='output',help='Output file, defaults to compiled_data-(day)-(month)-(hour)-(minute) if none given',default=None)


    options = parser.parse_args()
    inputs = options.inputs
    if inputs is None:
        inputs = [os.path.abspath('../')]
    inputs_names = [os.path.abspath(input).split('/')[-1] for input in inputs]
    inputs = [os.path.abspath(input) for input in inputs]
    known_barriers = options.known_barriers
    if known_barriers is not None:
        known_barriers = str(known_barriers[0])
        known_barriers = json.loads(known_barriers)

    output = options.output
    if output is None:
        date = datetime.now()
        date = '{0}-{1}-{2}-{3}'.format(date.day,date.month,date.hour,date.minute)
        if os.getcwd().split('/')[-1] == 'utilities' and len(inputs) == 1:
            output = '{1}/compiled_results_{0}.xlsx'.format(date,inputs[0])
        else:
            output = 'compiled_results_{0}.xlsx'.format(date)

        
    print('Writing output to {0}'.format(output))
    writer = pd.ExcelWriter(output,engine='xlsxwriter')


    #check they exist first
    for input in inputs:
        if not os.path.isdir(input):
            print("{0} directory could not be found!".format(input))
            exit()
    
    summaries = []
    for (input,input_name) in zip(inputs,inputs_names):

        inputdir = '{0}/input'.format(input) 
        if not os.path.isdir(inputdir):
            print("No input directory at {0}".format(inputdir))
            exit()
        mols = []
        types=('*.log','*.xyz')
        for ext in types:
            mols.extend(glob.glob(join(inputdir,ext)))

        mols = [mol.split('/')[-1].split('.')[0] for mol in mols]
        print('Reading {0} from {1}'.format(mols,input))
        
        files = [None]*len(mols)
        
        if os.path.isdir('{0}/benchmarking'.format(input)):
            benchmarkdir='{0}/benchmarking'.format(input)
            print('Reading benchmarking in {0}'.format(benchmarkdir))
            for x,mol in enumerate(mols):
                molfiles=[]
                molfiles.extend(glob.glob(join(benchmarkdir,'{0}-*.com'.format(mol))))
                files[x] = molfiles

         
         
        #initialize data frames to match EZ-TS requests

        barrier_columns = [com.split('{0}-'.format(mols[0]))[-1].split('.')[0] for com in files[0]]
        barrier_columns.sort()
        index = mols 
       
        barriers = pd.DataFrame(columns=barrier_columns,index=index).astype('object')

        #frequency information
        freq_columns = ['{0}_TS-Freq'.format(col) for col in barrier_columns]
        freq_columns.extend(['{0}_TS-niFreq'.format(col) for col in barrier_columns])
        freq_columns.extend(['{0}_R-niFreq'.format(col) for col in barrier_columns])
        freq_columns.sort()

        freqs = pd.DataFrame(columns=freq_columns,index=mols)

        #geometry information
        geom_columns = ['{0}_TS-CNNC'.format(col) for col in barrier_columns]
        geom_columns.extend(['{0}_R-CNNC'.format(col) for col in barrier_columns])
        geom_columns.sort() 
         
        geom = pd.DataFrame(columns=geom_columns,index=mols)

        #add columns for properies and other information to store
        other_columns = ['{0}_freq-time'.format(col) for col in barrier_columns]            
        other_columns.sort()
        index = mols 

        other = pd.DataFrame(columns=other_columns,index=index)
          

        #set up directory to gather cis/trans structures
        if not os.path.isdir('{0}/cis'.format(input)):
            os.mkdir('{0}/cis'.format(input))
        if not os.path.isdir('{0}/trans'.format(input)):
            os.mkdir('{0}/trans'.format(input))

        #Get barriers
        cis = get_cis(barriers,input)
        ts,freqs,times,max_angles = get_ts(barriers,input)
        barriers = get_barriers(barriers,ts,cis,input)


        #aggregate statistics
            #desired statistics columns, methods as rows:
            # ME, MAE, ninversion, nrotation, avg freq time, had errors

        if known_barriers is not None:
            ME_agg = barriers.aggregate(ME,0,mols,known_barriers).values
            MAE_agg = barriers.aggregate(MAE,0,mols,known_barriers).values
        else:
            ME_agg = ['NaN']*len(barriers.columns)
            MAE_agg = ['NaN']*len(barriers.columns)

        time_agg = times.aggregate(np.mean,0).values

        #bin the frequencies and assign labels - FALSE is rotation TRUE is inversion
        mechanism_labels = max_angles > 170.
        inversion_agg = mechanism_labels.aggregate(count_inversion,0).values
        min_freq = freqs.aggregate(np.amax,0).values
        rotation_agg = mechanism_labels.aggregate(count_rotation,0).values
        NaN_per_col = [max_angles[col].isna().sum() for col in barriers.columns]
        NaN_per_col = np.array(NaN_per_col)
        rotation_agg = np.subtract(rotation_agg,NaN_per_col) 
        max_freq = freqs.aggregate(np.amin,0).values

        #look to see if methods appeared in the manual fix files



        #put together aggregated data
        aggregated = pd.DataFrame(data = [ME_agg,MAE_agg,time_agg,inversion_agg,min_freq,rotation_agg,max_freq],index = ['me','mae','mean_frequency_time_(min)','n_inversion_(cnn>170)','max_frequency','n_rotation_(cnn<170)','min_frequency'],columns = barriers.columns).T
        
 
        #calculate ME, MAE (old style, added to barrier sheet)
        if known_barriers is not None:
            barriers.insert(0,'Experiment',[known_barriers[mol] for mol in mols])
            barriers.loc['MAE'] = ''
            nmol = len(mols)
            for col in barriers.columns:
                if col != 'Experiment':
                    total = 0
                    for index in range(0,nmol):
                        if not np.isnan(float(barriers[col][index])):
                            total += np.absolute(barriers['Experiment'][index] - barriers[col][index])
                    mae = total/float(nmol)
                    barriers.at['MAE',col] = mae
                    
        #put all the information toegether with each input dir on a different excel sheet
        barriers.to_excel(writer,sheet_name='{0}-Barriers'.format(input_name))
        #freqs.to_excel(writer,sheet_name='{0}-Freqs'.format(input))
        #max_angles.to_excel(writer,sheet_name='{0}-max_angles'.format(input))
        #times.to_excel(writer,sheet_name='{0}-time'.format(input))
        aggregated.to_excel(writer,sheet_name='{0}-summary'.format(input_name))
        
        summaries.append(aggregated)

    #combine all individual summaries into one
    if len(inputs) > 1:
        full_summary = pd.DataFrame().reindex_like(summaries[0])    
        for index,row in full_summary.iterrows():
            # ['me','mae','mean_frequency_time_(min)','n_inversion_(cnn>170)','max_frequency','n_rotation_(cnn<170)','min_frequency']
            if known_barriers is not None:
                me = np.mean([summary['me'][index] for summary in summaries]) 
                mae = np.mean([summary['mae'][index] for summary in summaries])
            else:
                me = 'NaN'
                mae = 'NaN'
            time = np.mean([summary['mean_frequency_time_(min)'][index] for summary in summaries])
            n_inversion = np.sum([summary['n_inversion_(cnn>170)'][index] for summary in summaries])
            max_frequency = np.amax([summary['max_frequency'][index] for summary in summaries]) 
            n_rotation = np.sum([summary['n_rotation_(cnn<170)'][index] for summary in summaries])
            min_frequency = np.amin([summary['min_frequency'][index] for summary in summaries])

            row_values = [me,mae,time,n_inversion,max_frequency,n_rotation,min_frequency]
            full_summary.loc[index] = row_values
          
        full_summary.to_excel(writer,sheet_name='Summary')
       
      

    writer.save()

    


if __name__ == "__main__":
    main()

