from __future__ import annotations

import numpy as np
import pandas as pd


class HOM:
    """
    Weak Coherent Pulse HOM interference.

    Input
    -----
    overlap.csv

    Output
    ------
    hom.csv

    Appends

        alpha_real
        alpha_imag

        beta_real
        beta_imag

        left_field_real
        left_field_imag

        right_field_real
        right_field_imag

        left_intensity
        right_intensity

        left_click_probability
        right_click_probability

        coincidence_probability
    """

    def __init__(

        self,

        eta_left=0.25,
        eta_right=0.25,

    ):

        self.eta_left = eta_left
        self.eta_right = eta_right

    # =====================================================

    def coherent_state(

        self,

        mu,
        phase,

    ):

        return np.sqrt(mu) * np.exp(

            1j * phase

        )

    # =====================================================

    def detector_probability(

        self,

        intensity,
        eta,

    ):

        return 1.0 - np.exp(

            -eta * intensity

        )

    # =====================================================

    def process(

        self,

        input_csv,
        output_csv,

    ):

        #
        # Read CSV
        #

        table = pd.read_csv(input_csv)

        #
        # Convert to NumPy
        #

        mu_a = table["alice_mu"].to_numpy(dtype=float)
        phi_a = table["alice_phase"].to_numpy(dtype=float)

        mu_b = table["bob_mu"].to_numpy(dtype=float)
        phi_b = table["bob_phase"].to_numpy(dtype=float)

        overlap = table["total_overlap"].to_numpy(dtype=float)

        #
        # Weak coherent states
        #

        alpha = np.sqrt(mu_a) * np.exp(1j * phi_a)

        beta = np.sqrt(mu_b) * np.exp(1j * phi_b)

        #
        # Apply indistinguishability
        #

        beta *= np.sqrt(overlap)

        #
        # 50:50 Beam Splitter
        #
        # |α>|β>
        #      ↓
        # |(α+β)/√2>|(α−β)/√2>
        #

        left = (

            alpha + beta

        ) / np.sqrt(2)

        right = (

            alpha - beta

        ) / np.sqrt(2)

        #
        # Output intensities
        #

        I_left = np.abs(left) ** 2

        I_right = np.abs(right) ** 2

        #
        # Threshold detector click probabilities
        #
        # P = 1-exp(-ηI)
        #

        P_left = 1.0 - np.exp(

            -self.eta_left * I_left

        )

        P_right = 1.0 - np.exp(

            -self.eta_right * I_right

        )

        #
        # Coincidence probability
        #

        P_coin = P_left * P_right

        #
        # Append to dataframe
        #

        table["alpha_real"] = np.real(alpha)
        table["alpha_imag"] = np.imag(alpha)

        table["beta_real"] = np.real(beta)
        table["beta_imag"] = np.imag(beta)

        table["left_field_real"] = np.real(left)
        table["left_field_imag"] = np.imag(left)

        table["right_field_real"] = np.real(right)
        table["right_field_imag"] = np.imag(right)

        table["left_intensity"] = I_left
        table["right_intensity"] = I_right

        table["left_click_probability"] = P_left
        table["right_click_probability"] = P_right

        table["coincidence_probability"] = P_coin

        #
        # Save
        #

        table.to_csv(

            output_csv,

            index=False,

        )

        return table