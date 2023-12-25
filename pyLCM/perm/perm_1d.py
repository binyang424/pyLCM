# -*- coding: utf-8 -*-
import numpy as np


def flow_dist(permeability, pressure, porosity, viscosity, time):
    """
    Calculate the one dimensional flow distance in porous media:
    distance = sqrt( (2* pressure * permeability * time) / (viscosity * porosity) )

    Parameters
    ----------
    permeability: float
        Permeability of porous media.
    pressure: float
        Injection pressure of the fluid.
    porosity: float
        Porosity of porous media.
    viscosity: float
        Viscosity of the fluid.
    time: float or list
        Filling time of porous media.

    Returns
    -------
    one dimensional flow distance
    """
    import numpy as np
    if isinstance(time, list):
        time = np.array(time)

    return np.sqrt((2 * pressure * permeability * time) / (viscosity * porosity))


def filling_time(permeability, pressure, porosity, viscosity, distance):
    """
    TODO: Check the formulation
    Calculate the filling time of porous media:
    fillingTime = (viscosity * porosity * distance^2) / (2 * pressure * permeability)

    Parameters
    ----------
    permeability: float
        Permeability of porous media.
    pressure:
        Pressure of the fluid.
    porosity:
    viscosity:
    :param distance:
    :return: filling time
    """
    return (viscosity * porosity * distance ** 2) / (2 * pressure * permeability)


def saturated(volumetric_flow_rate, area, pressure, flow_dist, mu):
    """
    Calculate the saturated one dimensional permeability of porous media according to
    the Darcy's law and experimental measured mass flow rate:

    permeability = (VolumeFlowRate * viscosity * thickness) / (pressure * area * liquidDensity)

        Parameters
        ----------
        volumetric_flow_rate: array-like
            Volumetric flow rate of the fluid in m^3/s.
        area: float
            Cross-section area perpendicular to the flow in m^2.
        pressure: float
            Pressure drop across the porous media in the flow direction in Pa.
        flow_dist: float
            Flow distance (sample length along the flow direction) in m.
        mu: float
            Viscosity of the fluid in Pa*s.

        Returns
        -------
        one dimensional permeability: m^2
    """

    if isinstance(volumetric_flow_rate, list):
        volumetric_flow_rate = np.array(volumetric_flow_rate)
    elif isinstance(volumetric_flow_rate, float):
        volumetric_flow_rate = np.array([volumetric_flow_rate])

    return (volumetric_flow_rate * mu * flow_dist) / (pressure * area)


def unsaturated(flow_front, time, Vf, pressure, mu, skip=0, plot=False):
    """
    Calculate the unsaturated permeability of a porous medium by recording the flow
    front position and the corresponding filling time. The injection is performed
    at a constant pressure.

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

    Examples
    --------
    >>> import pyLCM
    >>> import numpy as np
    >>> time = [0, 3, 8, 13, 20, 28, 34, 46, 57, 69, \
            82, 96, 109, 125, 142, 161, 180, 198, \
            218, 242, 262]
    >>> flow_front = [0, 0.02, 0.04, 0.06, 0.08, 0.1, \
                  0.12, 0.14, 0.16, 0.18, 0.20, 0.22, \
                  0.24, 0.26, 0.28, 0.30, 0.32, 0.34, \
                  0.36, 0.38, 0.4]
    >>> Vf = 0.5
    >>> pressure = 100000 # Pa
    >>> mu = 0.1 # Pa*s
    >>> perm = pyLCM.perm.perm_1d(flow_front, time, Vf, pressure, mu) # m^2
    >>> print(round(perm, 5))
    1.59596e-10
    """
    import numpy as np
    import matplotlib.pyplot as plt

    Lf_sq = np.square(flow_front)
    t = time[skip:]

    # Linear fitting: returns a vector of coefficients (slope,intercept)
    slope, intercept = np.polyfit(t, Lf_sq[skip:], 1)
    # r-square
    r_sq = np.corrcoef(t, Lf_sq[skip:])[0, 1] ** 2

    equation = np.poly1d([slope, intercept])  # retrieve the equation

    perm = (1 - Vf) * mu * slope / (2 * pressure)

    if plot:
        fig, ax = plt.subplots(dpi=300)

        ax.scatter(time, Lf_sq, color='y', label='Experiments')
        ax.plot(t, equation(t), color='r', label='Linear fitting')

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


def perm_scale(k, f_s):
    """
    Permeability estimation of scaled porous media.

    Notes
    -----
    Belot, Igor, et al. "A 3D additive manufacturing approach for the
    validation of a numerical wall-scale model of catalytic particulate
    filters." Chemical Engineering Journal 405 (2021): 126653.

    Parameters
    ----------
    k : float
        Permeability of the unscaled porous media.
    f_s : float
        Scaling factor of the porous media.

    Returns
    -------
    k_s : float
        Permeability of the scaled porous media.
    """
    return k * f_s ** 2


def piston_flow_rate(velocity, cross_section_area=0.0048454, liquid_density=960, alg="mass"):
    """
    Calculate the flow rate of piston pumps according to its area
    and pumping action velocity.

    Parameters
    ----------
    velocity : float
        Pumping action velocity of the piston pump in m/s.
    cross_section_area : float
        Cross-section area of the piston pump (m^2).
    liquid_density : float
        Density of the liquid in kg/m^3.
    alg : str
        Algorithm to calculate the flow rate. Default is "mass".
        The other option is "volume".

    Returns
    -------
    flow_rate : float
        Flow rate of the piston pump.
    """
    if alg == "mass":
        return velocity * cross_section_area * liquid_density
    elif alg == "volume":
        return velocity * cross_section_area


def pressure_drop(q, area, mu, k):
    """
    Calculate the pressure drop of a flow thorugh a porous media
    with a given flow rate, cross-section area and viscosity based
    on Darcy's law.

    Parameters
    ----------
    q: float
        Flow rate in m^3/s
    area: float
        Cross-section area perpendicular to the flow in m^2.
    mu: float
        Viscosity of the fluid in Pa*s.
    k: float
        Permeability of the porous media in m^2.

    Returns
    -------
    dp: float
        Pressure drop across the porous media in Pa.
    """

    return q * mu / (area * k)


if __name__ == "__main__":
    k = 1e-11  # m^2
    p = 1e5  # Pa
    phi = 0.5  # porosity
    mu = 0.1  # Pa*s
    s = 1  # m
    print("The flow distance at 25000 seconds is {}".format(flow_dist(k, p, phi, mu, 25000)))
    print("The one dimensional filling time for a 1 meter length porous meida is {}".format(
        filling_time(k, p, phi, mu, s)))

    q = 4.5019 / 1000  # kg/s
    p = 44697  # Pa
    mu = 0.118  # Pa*s
    h = 0.00301  # m
    A = 3.14159 * (57 / 1000) ** 2  # m^2
    rho = 960  # kg/m^3
    print(saturated(q, A, p, h, rho, mu))
