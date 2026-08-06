from __future__ import annotations

import numpy as np

from qkdengine.recorder.pulse_table import PulseTable


class Fiber:
    """
    Standard Single Mode Fiber.

    Applies

    • attenuation
    • propagation delay
    • phase noise
    • polarization rotation
    """

    C = 299792458.0

    def __init__(

        self,

        length_km: float,

        attenuation_db_per_km: float,

        refractive_index: float,

        phase_noise_std: float,

        polarization_std: float,

        rng=None,

    ):

        self.length_km = length_km

        self.alpha = attenuation_db_per_km

        self.n = refractive_index

        self.phase_noise_std = phase_noise_std

        self.polarization_std = polarization_std

        self.rng = (

            np.random.default_rng()

            if rng is None

            else rng

        )

    # ---------------------------------------------------------

    @property
    def transmission(self):

        return 10 ** (

            -(

                self.alpha

                * self.length_km

            )

            / 10

        )

    # ---------------------------------------------------------

    @property
    def propagation_delay(self):

        return (

            self.length_km

            * 1000

            * self.n

            / self.C

        )

    # ---------------------------------------------------------

    def process(

        self,

        table: PulseTable,

    ) -> PulseTable:

        df = table.df

        N = len(df)

        #
        # attenuation
        #

        df["mu"] *= self.transmission

        df["power_dbm"] -= (

            self.alpha

            * self.length_km

        )

        #
        # propagation delay
        #

        df["arrival_time"] = (

            df["timestamp"]

            + self.propagation_delay

        )

        #
        # phase noise
        #

        df["phase"] += self.rng.normal(

            0,

            self.phase_noise_std,

            N,

        )

        #
        # polarization rotation
        #

        theta = self.rng.normal(

            0,

            self.polarization_std,

            N,

        )

        px = df["polarization_x"].to_numpy()

        py = df["polarization_y"].to_numpy()

        df["polarization_x"] = (

            px*np.cos(theta)

            -

            py*np.sin(theta)

        )

        df["polarization_y"] = (

            px*np.sin(theta)

            +

            py*np.cos(theta)

        )

        return table