import pyLCM
import numpy as np

"""Input parameters"""
velocity = 25 * 10 ** (-3) / 60  # Injection (piston action) velocity in m^3/s.
density = 960  # liquid density, kg/m^3.
mu = 0.1  # Pa*s
scale = 5  # scale factor for the porous media.

"""Flow information"""
# piston cross-section area
area = (82.55 ** 2 - 25.4 ** 2) * np.pi / 4 * 10 ** (-6)  # m^2
# flow rate
q = pyLCM.perm.piston_flow_rate(velocity, area, density, "volume")

""""Sample information"""
# Sample area (3d printed)
area_sample = 12 * 15 * 10 ** (-6) * scale ** 2  # m^2
# sample thickness
t_sample = 5 * 10 ** (-3) * scale  # m
# sample permeability
k_sample = pyLCM.perm.perm_scale(8 * 10 ** (-12), scale)

"""Results"""
grad_p = pyLCM.perm.pressure_drop_1d(q, area_sample, mu, k_sample)
# pressure gradient
dp = grad_p * t_sample

# reynolds number
re = pyLCM.utility.reynolds_number(velocity / 0.5, density, mu, 0.5 / 1000 * scale)

print("The pressure drop and the flow reynolds number are: {} kPa and {}.".format(
    round(dp / 1000, 0), round(re, 4)))

"""Output"""
#             80                        50                       25
# fs = 1, 2243.2 kPa and 0.013;   1402.0 kPa and 0.008;     701.0 kPa and 0.004;
# fs = 2, 280.8 kPa and 0.026;    175.0 kPa and 0.016;      88.0 kPa and 0.008;
# fs = 3, 83.2 kPa and 0.038;     52.0 kPa and 0.024        26.0 kPa and 0.012;
# fs = 4, 35.2 kPa and 0.051;     22.0 kPa and 0.032;       11.0 kPa and 0.016;
# fs = 5, 17.6 kPa and 0.064;     11.0 kPa and 0.04;        6.0 kPa and 0.02;

import matplotlib.pyplot as plt

# font size: 12, font family: Times New Roman
plt.rcParams.update({'font.size': 12, 'font.family': 'Times New Roman'})
# figure size: 6.4 x 4.8 inches
plt.rcParams["figure.figsize"] = (5, 3.75)
# update the rcParams
plt.rcParams.update()

# plot re as a function of scaling factor fs
fs = np.arange(1, 6, 1)
re_80 = np.array([0.013, 0.026, 0.038, 0.051, 0.064])
re_50 = np.array([0.008, 0.016, 0.024, 0.032, 0.04])
re_25 = np.array([0.004, 0.008, 0.012, 0.016, 0.02])


plt.plot(fs, re_50, label="50 mm/min")
plt.plot(fs, re_25, label="25 mm/min")
plt.xlabel("Scaling factor")
plt.ylabel("Reynolds number")
plt.legend()
plt.tight_layout()
plt.show()