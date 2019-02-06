'''
Get SNR for the Table using Mat's covariance matrix
Note:
- Have an option to use cov mat with bid width of dl=300
- Have an option to use only the diagonal elements
- Scale cov mat with the right fsky via the relation: cov~1/fsky
'''
import numpy as np
from sn_forecast import LensingForecast
import matplotlib.pyplot as plt
import itertools

ClsCDM = np.loadtxt('data/May21_matter2lens_WF_CDM_cut_ibarrier_iconc_fCls.csv')
ClsFDM = np.loadtxt('data/May21_matter2lens_WF_FDM_1.0_cut_ibarrier_iconc_fCls.csv')

beams = [0.167]
fskys = [0.5,0.25,0.1]
noises = [0.5,0.25] 

diag = False
dl300 = True
date = '190119'
ksz = '' # options: '','reionKSZ_', 'bothKSZ_'

print 'date + if ksz: ',date,ksz

if dl300:
    dl300_str = '_dl300'
    print '--->Using dl300!'
else: dl300_str = ''
if diag: print '--->Just diagonal terms!'
print 'beam,fsky,noise,S/N'

for beam,fsky,noise in itertools.product(beams,fskys,noises):
    
    
    # Old code - 10arcsecond exp - bothKSZ
    ellBinEdges = np.load('data/'+date+'_experiment_'+str(beam)+'arc_'+str(noise)+'uk_2000_'+ksz+'2.912603855229585sqdeg_lbin_edges'+dl300_str+'.npy')
    ellMids  =  (ellBinEdges[1:] + ellBinEdges[:-1]) / 2
    
    cov = np.load('data/'+date+'_experiment_'+str(beam)+'arc_'+str(noise)+'uk_2000_'+ksz+'2.912603855229585sqdeg_covmat'+dl300_str+'.npy')
    cov = cov*2.912603855229585/41253./fsky # scale with the right fsky

    
    # Zero out off-diagonals
    if diag:
        for i in range(len(cov)):
            for j in range(len(cov)):
                if i!=j: cov[i,j] = 0

    # Calculate SNR squared
    LF = LensingForecast(ClsCDM,ClsFDM)
    sn2 = LF.SNR2_fromCov(cov,ellBinEdges)
    #print sn2
    print beam,fsky,noise,np.round(np.sqrt(np.sum(sn2)),0)
