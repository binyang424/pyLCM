# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt


def perm_1d(flow_front, time, Vf, pressure, mu, skip=0, plot=False):
    """
    Calculate the permeability of a porous medium by recording the flow front
    position and the corresponding filling time. The injection is performed
    at a constant pressure.

    TODO: the function is to be validated.

    Parameters
    ----------
    flow_front : list
        Flow front position in meter.
    time : list
        The time that the flow front position is recorded at the corresponding
        flow front position. The unit is second.
    Vf : float
        The fiber volume fraction of the porous media.
    pressure : float
        The pressure difference between the inlet and outlet of the porous media.
        The unit is Pascal.
    mu : float
        The viscosity of the fluid. The unit is Pascal second (Pa·s).
    skip : int, optional
        The number of data points to skip at the beginning of the data to cover
        the fully developed 1d flow only. The default is 0.
    plot : bool, optional
        Whether to plot the filling VS square of flow distance. The default is
        False.

    Returns
    -------
    perm : float
        The permeability of the porous media. The unit is m^2.
    """

    Lf_sq = np.square(flow_front)
    t = time[skip:]

    # Linear fitting: returns a vector of coefficients (slope,intercept)
    fit_coefficients = np.polyfit(t, Lf_sq[skip:], 1)
    # r-square
    r_sq = np.corrcoef(t, Lf_sq[skip:])[0, 1] ** 2

    equation = np.poly1d(fit_coefficients)  # retrieve the equation

    perm = (1 - Vf) * mu * fit_coefficients[0] / (2 * pressure)

    if plot:
        fig, ax = plt.subplots(dpi=300)
        ax.scatter(time, Lf_sq, color='y', label='Experiments')
        ax.plot(t, np.polyval(fit_coefficients, t), color='r', label='Linear fitting')
        ax.set_title('Time $t$ VS Square of flow distance $L^2$')
        ax.set_xlabel('time(s)')
        ax.set_ylabel('Square of flow distance $L^2 (m^2)$')

        ax.text(np.mean(time) * 0.3, np.mean(Lf_sq) * 1.5,
                'y={} \n\n $R^2$={}'.format(str(equation)[2:],
                                            round(r_sq, 3)),
                color='r', fontsize=10)
        plt.legend()
        plt.show()
    return perm


if __name__ == '__main__':
    time = [0, 3, 8, 13, 20, 28, 34, 46, 57, 69,
            82, 96, 109, 125, 142, 161, 180, 198,
            218, 242, 262]

    flow_front = [0, 0.02, 0.04, 0.06, 0.08, 0.1,
                  0.12, 0.14, 0.16, 0.18, 0.20, 0.22,
                  0.24, 0.26, 0.28, 0.30, 0.32, 0.34,
                  0.36, 0.38, 0.4]

    Vf, pressure, viscosity = 0.6946, 0.385e6, 0.25

    perm = perm_1d(flow_front, time, Vf, pressure, viscosity, skip=5, plot=True)

    print("The permeability of the porous media is: {} m^2".format(perm))
