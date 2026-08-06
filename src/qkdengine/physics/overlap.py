from __future__ import annotations

import numpy as np
import pandas as pd


class Overlap:
    """
    Computes pulse indistinguishability between Alice and Bob.

    Inputs
    ------
    Alice_Fiber.csv
    Bob_Fiber.csv

    Output
    ------
    overlap.csv

    The output contains ALL Alice variables,
    ALL Bob variables,
    and the newly computed overlap quantities.
    """

    def __init__(

        self,

        pulse_width: float = 500e-12,
        spectral_width: float = 1e-9,

    ):

        self.sigma_t = pulse_width
        self.sigma_lambda = spectral_width

    # =========================================================

    def temporal_overlap(
        self,
        dt,
    ):

        return np.exp(

            -(dt ** 2)

            /

            (4 * self.sigma_t ** 2)

        )

    # =========================================================

    def spectral_overlap(
        self,
        wl1,
        wl2,
    ):

        delta = wl1 - wl2

        return np.exp(

            -(delta ** 2)

            /

            (4 * self.sigma_lambda ** 2)

        )

    # =========================================================

    def polarization_overlap(
        self,
        ax,
        ay,
        bx,
        by,
    ):

        a = np.array([ax, ay], dtype=float)
        b = np.array([bx, by], dtype=float)

        a /= np.linalg.norm(a)
        b /= np.linalg.norm(b)

        return abs(np.vdot(a, b)) ** 2

    # =========================================================

    def process(

        self,

        alice_csv,
        bob_csv,
        output_csv,

    ):

        alice = pd.read_csv(alice_csv)
        bob = pd.read_csv(bob_csv)

        n = min(len(alice), len(bob))

        alice = alice.iloc[:n].copy()
        bob = bob.iloc[:n].copy()

        #
        # Rename Bob columns
        #

        bob.columns = [

            "bob_" + c

            if c != "pulse_id"

            else c

            for c in bob.columns

        ]

        #
        # Rename Alice columns
        #

        alice.columns = [

            "alice_" + c

            if c != "pulse_id"

            else c

            for c in alice.columns

        ]

        #
        # Merge
        #

        table = pd.concat(

            [

                alice,

                bob.drop(columns=["pulse_id"]),

            ],

            axis=1,

        )

        #
        # Allocate overlap arrays
        #

        temporal = np.zeros(n)
        spectral = np.zeros(n)
        polarization = np.zeros(n)
        total = np.zeros(n)

        # =====================================================
        # Compute overlaps
        # =====================================================

        for i in range(n):

            temporal[i] = self.temporal_overlap(

                table.loc[i, "alice_arrival_time"]

                -

                table.loc[i, "bob_arrival_time"]

            )

            spectral[i] = self.spectral_overlap(

                table.loc[i, "alice_wavelength"],

                table.loc[i, "bob_wavelength"],

            )

            polarization[i] = self.polarization_overlap(

                table.loc[i, "alice_polarization_x"],
                table.loc[i, "alice_polarization_y"],

                table.loc[i, "bob_polarization_x"],
                table.loc[i, "bob_polarization_y"],

            )

            total[i] = (

                temporal[i]

                *

                spectral[i]

                *

                polarization[i]

            )

        #
        # Append
        #

        table["temporal_overlap"] = temporal
        table["spectral_overlap"] = spectral
        table["polarization_overlap"] = polarization
        table["total_overlap"] = total

        #
        # Save
        #

        table.to_csv(

            output_csv,

            index=False,

        )

        return table