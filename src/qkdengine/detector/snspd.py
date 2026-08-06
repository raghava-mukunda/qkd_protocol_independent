from __future__ import annotations

import numpy as np

from qkdengine.recorder.pulse_table import PulseTable


class SNSPD:
    """
    Superconducting Nanowire Single Photon Detector.

    Converts optical intensity into detector clicks.

    P(click) = 1-exp(-ηI)

    Supports

        efficiency
        dark counts
        dead time (later)
    """

    def __init__(

        self,

        efficiency=0.95,

        dark_probability=2e-6,

        rng=None,

    ):

        self.efficiency = efficiency

        self.dark_probability = dark_probability

        self.rng = (

            np.random.default_rng()

            if rng is None

            else rng

        )

    # ---------------------------------------------------------

    def click_probability(

        self,

        intensity,

    ):

        return (

            1

            -

            np.exp(

                -self.efficiency * intensity

            )

        )

    # ---------------------------------------------------------

    def process(

        self,

        table: PulseTable,

    ):

        df = table.df

        left_prob = self.click_probability(

            df["left_intensity"].to_numpy()

        )

        right_prob = self.click_probability(

            df["right_intensity"].to_numpy()

        )

        #
        # Add dark counts
        #

        left_prob += self.dark_probability

        right_prob += self.dark_probability

        left_prob = np.clip(left_prob,0,1)

        right_prob = np.clip(right_prob,0,1)

        #
        # Monte Carlo
        #

        left_click = (

            self.rng.random(

                len(df)

            )

            <

            left_prob

        )

        right_click = (

            self.rng.random(

                len(df)

            )

            <

            right_prob

        )

        df["left_click_probability"] = left_prob

        df["right_click_probability"] = right_prob

        df["left_click"] = left_click

        df["right_click"] = right_click

        return table