

import math


def distance(permeability, pressure, porosity, viscosity, time):
    """
    Calculate the one dimensional flow distance in porous media:
    distance = sqrt( (2* pressure * permeability * time) / (viscosity * porosity) )
    :param permeability:
    :param pressure:
    :param porosity:
    :param viscosity:
    :return: one dimensional flow distance
    """
    return math.sqrt((2 * pressure * permeability * time) / (viscosity * porosity))


def fillingTime(permeability, pressure, porosity, viscosity, distance):
    """
    Calculate the filling time of porous media:
    fillingTime = (viscosity * porosity * distance^2) / (2 * pressure * permeability)
    :param permeability:
    :param pressure:
    :param porosity:
    :param viscosity:
    :param distance:
    :return: filling time
    """
    return (viscosity * porosity * distance ** 2) / (2 * pressure * permeability)


def perm1d(massFlowRate, area, pressure, thickness, liquidDensity, viscosity, algorithm="Darcy"):
    """
    Calculate the one dimensional permeability of porous media according to the Darcy's law and experimental measured mass flow rate:
    permeability = (VolumeFlowRate * viscosity * thickness) / (pressure * area * liquidDensity)
    :param algorithm:
    :param massFlowRate: kg/s
    :param area: m^2
    :param pressure: Pa
    :param thickness: m
    :param liquidDensity: kg/m^3
    :return: one dimensional permeability: m^2
    """
    if algorithm == "Darcy":
        return (massFlowRate * viscosity * thickness) / (pressure * area * liquidDensity)
    elif algorithm == "Darcy2":
        return (massFlowRate * area) / (pressure * thickness * liquidDensity)
    else:
        raise Exception("algorithm is not defined")


if __name__ == "__main__":
    k = 1e-11;  # m^2
    p = 1e5;    # Pa
    phi = 0.5   # porosity
    mu = 0.1    # Pa*s
    s = 1    # m
    print("The flow distance at 25000 seconds is {}".format(distance(k, p, phi, mu, 25000)))
    print("The one dimensional filling time for a 1 meter length porous meida is {}".format(
        fillingTime(k, p, phi, mu, s)))

    q = 4.5019 / 1000  # kg/s
    p = 44697       # Pa
    mu = 0.118   # Pa*s
    h = 0.00301 # m
    A = 3.14159 * (57 / 1000) ** 2 # m^2
    rho = 960   # kg/m^3
    print(perm1d(q, A, p, h, rho, mu, algorithm="Darcy"))
