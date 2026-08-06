from __future__ import annotations

import numpy as np

from qkdengine.recorder.pulse_table import PulseTable


class OpticalDelayLine:
    """
    Motorized Optical Delay Line.

    Compensates timing mismatch between Alice and Bob.

    Input
    -----
    Alice PulseTable
    Bob PulseTable

    Output
    ------
    Updated Bob PulseTable

    Modifies
    --------
    arrival_time

    Appends
    -------
    timing_error_before
    timing_error_after
    """

    def __init__(

        self,

        delay=0.0,

    ):

        #
        # Delay applied to Bob
        #

        self.delay = delay

    # ---------------------------------------------------------

    def process(

        self,

        alice: PulseTable,

        bob: PulseTable,

    ):

        A = alice.df
        B = bob.df

        N = min(

            len(A),

            len(B),

        )

        before = (

            B.loc[:N-1, "arrival_time"].to_numpy()

            -

            A.loc[:N-1, "arrival_time"].to_numpy()

        )

        #
        # Apply delay
        #

        B.loc[:N-1, "arrival_time"] += self.delay

        after = (

            B.loc[:N-1, "arrival_time"].to_numpy()

            -

            A.loc[:N-1, "arrival_time"].to_numpy()

        )

        #
        # Save diagnostics
        #

        B["timing_error_before"] = before

        B["timing_error_after"] = after

        return alice, bob