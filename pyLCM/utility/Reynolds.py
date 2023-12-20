import numpy as np


def reynolds_number(rho, u, L, mu):
    """
    Calculate Reynolds number for a given velocity field.

    .. image:: ../image/reynolds_number.svg

    Parameters
    ----------
    rho : float
        Density of fluid
    u : float or array of float/vector
        Velocity vector (field) of fluid
    L : float
        Characteristic length
    mu : float
        Dynamic viscosity of fluid

    Returns
    -------
    Re : float
        Reynolds number
    """

    return rho * np.linalg.norm(u) * L / mu
