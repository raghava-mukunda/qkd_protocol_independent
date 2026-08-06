from __future__ import annotations

import numpy as np

from qkdengine.recorder.pulse_table import PulseTable


class Charlie:
    """
    Charlie relay.

    Charlie performs NO optics.

    He simply observes detector clicks and publicly announces

        LEFT
        RIGHT
        DOUBLE
        NONE

    Bell-state success occurs only for
    single detector clicks.
    """

    def process(

        self,

        table: PulseTable,

    ) -> PulseTable:

        df = table.df

        N = len(df)

        detector = np.full(

            N,

            "NONE",

            dtype=object,

        )

        bell_state = np.full(

            N,

            "",

            dtype=object,

        )

        success = np.zeros(

            N,

            dtype=bool,

        )

        left = df["left_click"].to_numpy()

        right = df["right_click"].to_numpy()

        #
        # Single LEFT click
        #

        mask = left & (~right)

        detector[mask] = "LEFT"

        bell_state[mask] = "PSI_PLUS"

        success[mask] = True

        #
        # Single RIGHT click
        #

        mask = (~left) & right

        detector[mask] = "RIGHT"

        bell_state[mask] = "PSI_MINUS"

        success[mask] = True

        #
        # Double click
        #

        mask = left & right

        detector[mask] = "DOUBLE"

        bell_state[mask] = ""

        success[mask] = False

        #
        # Save
        #

        df["detector"] = detector

        df["bell_state"] = bell_state

        df["bell_success"] = success

        return table