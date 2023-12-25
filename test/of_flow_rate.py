import numpy as np
import matplotlib.pyplot as plt
import pyLCM as lcm
import os

""" Read flow rate """
path = "./2/TG96N_Vf54_134_200_236/postProcessing/" \
       "flowRatePatch/0/surfaceFieldValue.dat"
skip = 10

""" Physical properties of fluid """
rho = 1000  # kg/m3
nu = 1e-4  # m2/s
mu = rho * nu  # Pa.s

""" Boundary conditions """
pressure = 1 * rho  # Pa
# flowLength = 0.0114   # m, Kx
# flowLength = 0.01312  # m, Ky
flowLength = 0.0097  # m, Kz

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

try:
    while True:
        # clear terminal when run python file
        os.system('cls' if os.name == 'nt' else 'clear')

        data = lcm.of_tools.read_flow_rate(path)
        area = data["area"]  # m2

        flow_rate = data["flow rate"]

        """ Calculate permeability """
        permeability = np.round(lcm.perm_1d.saturated(flow_rate[-100::15, 1], area, pressure, flowLength, mu), 14)

        print(lcm.bcolors.header("Area: "), f"{area} m^2")
        print(lcm.bcolors.header("Permeability: "), *permeability, " m^2")

        u = flow_rate[:, 1] / area  # m/s
        print(lcm.bcolors.header("Reynolds number: "), lcm.reynolds_number(rho, u[-100::15], 2e-3, mu))

        ax.plot(np.arange(skip, flow_rate.shape[0]), flow_rate[skip:, 1])
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Volumetric flow rate ($m^3/s$)")
        fig.canvas.draw()
        plt.pause(5)
        plt.cla()  # clear previous data

except KeyboardInterrupt:
    plt.savefig("flow_rate.jpg", dpi=600)
    print(lcm.bcolors.ok("Figure is saved. The program is terminated by user."))
    plt.close()