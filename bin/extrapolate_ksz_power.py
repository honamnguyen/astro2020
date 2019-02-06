'''
Usage: take in ksz power and extroplate
Method: extroplate the linearity in ell^2 * C_ksz_power
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

ell,ksz = np.loadtxt('data/reionization_ksz.txt',unpack=True)
# ksz += np.loadtxt('data/late_ksz.txt',unpack=True)[1] # uncomment to get both ksz power

ell = ell[1:]
ksz = ksz[1:]
newell = np.arange(1,50000)

ell2ksz = interp1d(ell,ell**2*ksz,kind='cubic',bounds_error=False,fill_value='extrapolate')

# plot extrapolation of ell^2 * C_ksz_power
plt.plot(ell,ell**2*ksz)
plt.plot(newell,ell2ksz(newell),'--')
plt.show()

# plot extrapolation of C_ksz_power
plt.loglog(ell,ksz)
plt.loglog(newell,ell2ksz(newell)/newell**2,'--')
plt.show()

np.savetxt('output/reion_ksz_extrapolate.txt',np.vstack([newell,ell2ksz(newell)/newell**2]).T)
#np.savetxt('output/both_ksz_extrapolate.txt',np.vstack([newell,ell2ksz(newell)/newell**2]).T)
