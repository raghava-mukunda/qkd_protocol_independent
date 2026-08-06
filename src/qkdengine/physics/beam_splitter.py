from __future__ import annotations

import numpy as np

from qkdengine.recorder.pulse_table import PulseTable


class BeamSplitter:
    """
    Ideal 50:50 Beam Splitter.

    Inputs
    ------
    Alice PulseTable
    Bob PulseTable

    Outputs
    -------
    Updates BOTH tables with

        left_field_real
        left_field_imag

        right_field_real
        right_field_imag

        left_intensity
        right_intensity

    Physics
    -------

        E_L = (Ea + Eb)/sqrt(2)

        E_R = (Ea - Eb)/sqrt(2)

    """

    def process(

        self,

        alice: PulseTable,

        bob: PulseTable,

    ):

        a = alice.df
        b = bob.df

        N = min(

            len(a),

            len(b),

        )

        #
        # Coherent amplitudes
        #

        alpha = (

            np.sqrt(

                a.loc[:N-1, "mu"].to_numpy()

            )

            *

            np.exp(

                1j *

                a.loc[:N-1, "phase"].to_numpy()

            )

        )

        beta = (

            np.sqrt(

                b.loc[:N-1, "mu"].to_numpy()

            )

            *

            np.exp(

                1j *

                b.loc[:N-1, "phase"].to_numpy()

            )

        )

        #
        # 50:50 Beam Splitter
        #

        left = (

            alpha + beta

        ) / np.sqrt(2)

        right = (

            alpha - beta

        ) / np.sqrt(2)

        #
        # Intensities
        #

        I_left = np.abs(left)**2

        I_right = np.abs(right)**2

        #
        # Save to BOTH tables
        #

        for table in (a, b):

            table["left_field_real"] = np.real(left)

            table["left_field_imag"] = np.imag(left)

            table["right_field_real"] = np.real(right)

            table["right_field_imag"] = np.imag(right)

            table["left_intensity"] = I_left

            table["right_intensity"] = I_right

        return alice, bob