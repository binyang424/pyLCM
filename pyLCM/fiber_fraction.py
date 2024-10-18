import numpy as np

class FiberFraction:
    def __init__(self, tow_cross_section_area, n_fibers, d_fiber):
        self.tow_cross_section_area = tow_cross_section_area
        self.n_fibers = n_fibers
        self.d_fiber = d_fiber

    def tow_vf(self, physical_checking=False):
        """
        Calculate the fiber volume fraction of a fiber tow according to
        fiber numbers it containing and the fiber diameter.

            Parameters
            ----------
            tow_cross_section_area : float or list of float
                Cross-sectional area of the fiber tow.
            n_fibers : int
                Number of fibers in the tow.
            d_fiber : float
                Diameter of the fiber.
            physical_checking : bool, optional
                If True, the fiber volume fraction will be checked to be in the
                range of 0 to 0.907 for hexagonal close packing. The default is False.

            Returns
            -------
            vf : float or list of float
                local fiber volume fractions of the fiber tow.
        """
        vf = self.n_fibers * np.pi * (1 / 2 * self.d_fiber) ** 2 / self.tow_cross_section_area

        limit = np.pi/2/np.sqrt(3)  # for hexagonal packing of cylindrical fibers
        if np.any(vf > limit) and physical_checking:
            raise ValueError("fiber volume fraction cannot be larger than the "
                            "limit of hexagonal packing (%.2f)" % limit)
        return vf

    def solid_vf(self, volume_tows, volume_total):
        """
        Calculate the solid volume fraction (the fiber tows are regared as solid)
        of a given volume (unit cell). The result can also be interpreted as the
        complementary of the volume fraction of meso-pores between the fiber tows.
        Namely, the solid volume fraction = 1 - volume fraction of meso-pores.

            Parameters
            ----------
            volume_tows : float or list of float
                Volume of the fiber tows which are regared as solid.
            volume_total : float
                Volume of the composite.

            Returns
            -------
            vf : float or list of float
                Solid volume fraction of given volume.
            """
        return volume_tows / volume_total

    def vf_preform(self, rho_areal, n_layers
                    , thickness, rho_fiber=2550):
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


def tex_to_area(tex, density_fiber=2550):
    """
    Calculate the cross-sectional area of fibers containing in a tow according
    to the tow linear density in tex and the fiber diameter, where:

    .. math::
        1 tex = 1/1000 * kg/km

        Note
        ------
        This function is used to calculate the cross-sectional area of fibers only
        when the fiber diameter and number of fiber is not available. If the fiber
        diameter is known, the cross-sectional area of fibers can be calculated
        using thees information directly.

        Parameters
        ----------
        tex : float
            Tow linear density in tex.
        density_fiber : float
            Density of the fiber in kg/m^3.

        Returns
        -------
        area : float
            Cross-sectional area of fibers containing in a tow in mm^2.
    """
    return (tex * 1e-3) / (density_fiber * 1e3) * 1e6


def tow_vf(tow_cross_section_area, n_fibers, d_fiber, physical_checking=False):
    """
    Calculate the fiber volume fraction of a fiber tow according to
    fiber numbers it containing and the fiber diameter.

        Parameters
        ----------
        tow_cross_section_area : float or list of float
            Cross-sectional area of the fiber tow.
        n_fibers : int
            Number of fibers in the tow.
        d_fiber : float
            Diameter of the fiber.
        physical_checking : bool, optional
            If True, the fiber volume fraction will be checked to be in the
            range of 0 to 0.907 for hexagonal close packing. The default is False.

        Returns
        -------
        vf : float or list of float
            local fiber volume fractions of the fiber tow.
    """
    vf = n_fibers * np.pi * (1 / 2 * d_fiber) ** 2 / tow_cross_section_area

    limit = np.pi/2/np.sqrt(3)  # for hexagonal packing of cylindrical fibers
    if np.any(vf > limit) and physical_checking:
        raise ValueError("fiber volume fraction cannot be larger than the "
                         "limit of hexagonal packing (%.2f)" % limit)
    return vf


def solid_vf(volume_tows, volume_total):
    """
    Calculate the solid volume fraction (the fiber tows are regared as solid)
    of a given volume (unit cell). The result can also be interpreted as the
    complementary of the volume fraction of meso-pores between the fiber tows.
    Namely, the solid volume fraction = 1 - volume fraction of meso-pores.

        Parameters
        ----------
        volume_tows : float or list of float
            Volume of the fiber tows which are regared as solid.
        volume_total : float
            Volume of the composite.

        Returns
        -------
        vf : float or list of float
            Solid volume fraction of given volume.
        """
    return volume_tows / volume_total


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
    tow_cross_section_area = (2 / 2) ** 2 * np.pi
    n_fibers = 1
    d_fiber = 1.5
    vf = tow_vf(tow_cross_section_area, n_fibers, d_fiber)
    print(vf)
