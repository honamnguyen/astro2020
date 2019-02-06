'''
Make noise curves and get delensing efficiency
'''
import sys, os
from ConfigParser import SafeConfigParser 
import cPickle as pickle
import numpy as np
from scipy.interpolate import interp1d
import argparse
from pyfisher.lensInterface import lensNoise
from orphics.io import list_from_config, cprint
import orphics.cosmology as cosmo
#from orphics.cosmology import LensForecast

# Get the name of the experiment and lensing type from command line
parser = argparse.ArgumentParser(description='Run a Fisher test.')
parser.add_argument('expName', type=str,help='The name of the experiment in input/params.ini')
parser.add_argument('lensName',type=str,help='The name of the CMB lensing section in input/params.ini. ',default="")
#parser.add_argument('saveName', nargs='?',type=str,help='Suffix for plots ',default="")
parser.add_argument('saveName',type=str,help='Suffix for plots ',default="")

args = parser.parse_args()
expName = args.expName
lensName = args.lensName
saveName = args.saveName
print expName,lensName,saveName

TCMB = 2.7255e6
bigell = 50000
gradCut = 50000
deg = 5

# Read config
iniFile = "input/params.ini"
Config = SafeConfigParser()
Config.optionxform=str
Config.read(iniFile)

#fskyList = ['04000','08000','16000']
#noiseList = ['SENS0','SENS1','SENS2']
nIter = np.inf

if nIter == 1:
    iterName = '_iterOff'
else:
    iterName = '_iterOn'

#mnus = np.zeros([len(fskyList),len(noiseList)])
print "Run with testNlkk lensing or lensTT ",iterName
outDir = 'output/'+saveName+'_'
#for noiseNow,fskyNow in zip(noiseList,fskyList):
i = 0

#cambRoot = 'data/Aug6_highAcc_CDM'
cambRoot = '../quicklens/quicklens/data/cl/planck_wp_highL/planck_lensing_wp_highL_bestFit_20130627'
#cambRoot = '/home/hnnguyen/CAMB-0.1.6.1/base_plikHM_TT_lowTEB_minimum_fudgedtotaup06_lmax5000'
theoryOverride = cosmo.loadTheorySpectraFromCAMB(cambRoot,unlensedEqualsLensed=False,useTotal=False,TCMB = TCMB,lpad=bigell) #,get_dimensionless=True)
#theoryOverride = None

'''
# Get CMB noise and pad it with inf
tellmin,tellmax = list_from_config(Config,expName,'tellrange')
pellmin,pellmax = list_from_config(Config,expName,'pellrange')
ellT,nlTT,dummy = np.loadtxt('tests/TT/SOV3_T_default1-4-2_noisecurves_deproj1_'+noiseNow+'_mask_'+fskyNow+'_ell_TT_yy.txt',unpack=True)
ellE,nlEE,nlBB = np.loadtxt('tests/EE-BB/SOV3_pol_default1-4-2_noisecurves_deproj1_'+noiseNow+'_mask_'+fskyNow+'_ell_EE_BB.txt',unpack=True)
fnTT = cosmo.noise_pad_infinity(interp1d(ellT,nlTT,bounds_error=False,fill_value=np.inf),tellmin,tellmax)
fnEE = cosmo.noise_pad_infinity(interp1d(ellE,nlEE,bounds_error=False,fill_value=np.inf),pellmin,pellmax)
'''     
# fnTT is dimensional from file        
# Pad CMB lensing noise with infinity outside L ranges

tellmin,tellmax = list_from_config(Config,expName,'tellrange')
pellmin,pellmax = list_from_config(Config,expName,'pellrange')
px = np.round(180./max(tellmax,pellmax)*60.*0.95,2)
                
ls,Nls,ellbb,dclbb,efficiency,cc = lensNoise(Config,expName,lensName,beamOverride=None,lkneeTOverride=None,lkneePOverride=None,alphaTOverride=None,alphaPOverride=None,deg=deg,px=px,gradCut=gradCut,bigell=bigell,theoryOverride=theoryOverride,noiseFuncT=None,noiseFuncP=None,nIter=nIter)

kellmin,kellmax = list_from_config(Config,lensName,'Lrange')
fnKK = cosmo.noise_pad_infinity(interp1d(ls,Nls,fill_value=np.inf,bounds_error=False),kellmin,kellmax)
Lrange = np.arange(kellmin,kellmax)
#np.savetxt(outDir+'nlkk'+iterName+'.csv',np.vstack([Lrange,fnKK(Lrange)]).T)
cprint("Delensing efficiency: "+ str(efficiency) + " %",color="green",bold=True)
                        
#j+=1
#i+=1

