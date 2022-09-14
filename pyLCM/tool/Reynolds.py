import numpy as np

def ReynoldsNumber(velocity, density, viscosity, length):
    """
    Calculate Reynolds number for a given velocity field.
        Re = rho * u * L / mu
    :param velocity: float or array_like, velocity field
    :param density: float, density of fluid
    :param viscosity: float, dynamic viscosity of fluid
    :param length: characteristic length
    :return: Reynolds number
    """
    return density * np.linalg.norm(velocity) * length / viscosity
