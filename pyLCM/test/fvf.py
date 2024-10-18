import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def vf_preform(rho_areal, n_layers, thickness, rho_fiber=2550):
    """
    Calculate the fiber volume fraction of a preform according to
    areal density, number of layers and thickness of the preform.

    .. math::
        V_f = \\frac{n \\times \\rho_{areal}} { t \\times rho_{fiber}}

        Parameters
        ----------
        rho_areal : float
            Areal density of the reinforcement textile. Unit: kg/m^2.
        n_layers : int
            Number of layers of reinforcement textile in the preform.
        thickness : float
            Thickness of the preform. Unit: m.
        rho_fiber : float, optional
            Density of the fiber in kg/m^3. The default is 2550 kg/m^3.

        Returns
        -------
        vf : float
            Fiber volume fraction of the preform.
        """
    vf = rho_areal * n_layers / thickness / rho_fiber

    return vf


if __name__ == "__main__":
    # TG96N: rho_areal = 3250 g/m^2, n_layers = 4
    t = 0.015  # 15 mm
    delta_t = 0.0001  # 0.0001 m = 0.1 mm

    vf = 0
    vf_last = 0

    n_layer = 10
    rho_areal = 225  # 3250 g/m^2

    vf_thickness = pd.DataFrame(columns=["Thickness (mm)", "Vf", "delta_t (mm)", "Vf - Vf_last"])

    while vf_last < 0.55 and t > 0.002:
        vf = vf_preform(rho_areal / 1000, n_layer, t)

        if vf > vf_last and vf > 0.45:
            print(vf, t, vf - vf_last)
            vf_thickness = vf_thickness._append({"Thickness (mm)": t * 1000,
                                                "Vf": vf,
                                                "delta_t (mm)": delta_t * 1000,
                                                "Vf - Vf_last": vf - vf_last},
                                               ignore_index=True)

        t -= delta_t
        vf_last = vf