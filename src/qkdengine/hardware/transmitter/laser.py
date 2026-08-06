from __future__ import annotations

import numpy as np

from qkdengine.recorder.pulse_table import PulseTable


class Laser:
    """
    Digital twin of the CW DFB laser.

    Responsibilities
    ----------------
    • Generate N optical pulses
    • Assign timestamps
    • Assign wavelength
    • Assign linewidth
    • Assign initial optical power
    • Assign random optical phase
    • Assign initial polarization

    Does NOT perform

    - Intensity modulation
    - Phase modulation
    - Attenuation
    - Fiber propagation
    """

    def __init__(

        self,

        wavelength: float,

        linewidth: float,

        repetition_rate: float,

        output_power_dbm: float,

        polarization_angle_std: float = 0.0,

        rng: np.random.Generator | None = None,

    ):

        self.wavelength = wavelength

        self.linewidth = linewidth

        self.repetition_rate = repetition_rate

        self.output_power_dbm = output_power_dbm

        self.polarization_angle_std = polarization_angle_std

        self.rng = (

            np.random.default_rng()

            if rng is None

            else rng

        )

    # ---------------------------------------------------------

    def generate(

        self,

        number_of_pulses: int,

    ) -> PulseTable:

        table = PulseTable.create(

            number_of_pulses,

        )

        df = table.df

        #
        # Pulse timestamps
        #

        df["timestamp"] = (

            np.arange(number_of_pulses)

            / self.repetition_rate

        )

        #
        # Laser wavelength
        #

        df["wavelength"] = self.wavelength

        #
        # Linewidth
        #

        df["linewidth"] = self.linewidth

        #
        # Optical power
        #

        df["power_dbm"] = self.output_power_dbm

        #
        # Random optical phase
        #

        df["phase"] = self.rng.uniform(

            0.0,

            2.0 * np.pi,

            number_of_pulses,

        )

        #
        # Jones vector
        #

        theta = self.rng.normal(

            0.0,

            self.polarization_angle_std,

            number_of_pulses,

        )

        df["polarization_x"] = np.cos(theta)

        df["polarization_y"] = np.sin(theta)

        return table