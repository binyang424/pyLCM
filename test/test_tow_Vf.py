import pyLCM as lcm
import numpy as np

tow_cross_section_area = (2 / 2) ** 2 * np.pi
n_fibers = 1
d_fiber = 1.5
vf = lcm.utility.tow_vf(tow_cross_section_area, n_fibers, d_fiber)
print(vf)
