from __future__ import annotations

import numpy as np

from qkdengine.recorder.pulse_table import PulseTable


class PhaseModulator:
    """
    LiNbO3 Phase Modulator.

    Hardware model only.

    Applies an externally supplied phase to each pulse.
    The protocol layer decides what those phases are.
    """

    def __init__(

        self,

        rng: np.random.Generator | None = None,

    ):

        self.rng = (

            np.random.default_rng()

            if rng is None

            else rng

        )

    # ---------------------------------------------------------

    def process(

        self,

        table: PulseTable,

        phases=None,

    ) -> PulseTable:

        df = table.df

        N = len(df)

        #
        # If no phases supplied,
        # use random phases (temporary validation mode)
        #

        if phases is None:

            phases = self.rng.uniform(

                0,

                2 * np.pi,

                N,

            )

        phases = np.asarray(phases)

        if len(phases) != N:

            raise ValueError(

                "Phase array length does not match pulse table."

            )

        #
        # Update phase
        #

        df["phase"] = phases

        return table