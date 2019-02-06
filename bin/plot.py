import argparse
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('fileName', type=str)
args = parser.parse_args()

Nls = np.loadtxt(args.fileName)
plt.loglog(Nls[:,0],Nls[:,1])
#plt.plot(Nls[:,0],Nls[:,1])
plt.show()

