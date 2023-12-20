import numpy as np


def check_numeric(x):
    try:
        float(x)
        return True
    except:
        return False


def as_si(x, ndp):
    """
    Return x in scientific notation with n decimal places.

    Parameters
    ----------
    x : float
        The number to be converted.
    ndp : int
        Number of decimal places.

    Returns
    -------
    s : str
        The number in scientific notation with n decimal places.
    """
    s = '{x:0.{ndp:d}e}'.format(x=x, ndp=ndp)
    m, e = s.split('e')
    exp = int(e)
    return r'{m:s} $\times$ 10^'.format(m=m) + str(exp)
