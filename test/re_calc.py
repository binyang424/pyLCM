import pyLCM
import numpy as np

# Polytechnique
gamma_p = 0.351
A = 1

# Wuhan
gamma_p = 0.351
A = 1

phi = 0.4

v = 1
rho = 960  # kg/m3
mu = 0.101  # Pa.s
d = np.sqrt(1e-11)  # m

Re = pyLCM.utility.ReynoldsNumber(velocity=v, density=rho, viscosity=mu, length=d)
print(Re)
