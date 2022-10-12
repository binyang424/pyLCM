import numpy as np


def reynolds_number(velocity, density, viscosity, length):
    """
    Calculate Reynolds number for a given velocity field.

    .. image:: ../image/reynolds_number.svg

    Parameters
    ----------
    velocity: float or array_like
        velocity field
    density: float
        density of fluid
    viscosity: float
        dynamic viscosity of fluid
    length: float
        characteristic length

    Returns
    -------
    Reynolds number
    """
    return density * np.linalg.norm(velocity) * length / viscosity
