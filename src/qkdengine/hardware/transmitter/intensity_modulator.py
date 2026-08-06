from __future__ import annotations

import numpy as np

from qkdengine.recorder.pulse_table import PulseTable


class IntensityModulator:
    """
    LiNbO3 Intensity Modulator.

    Responsibilities
    ----------------
    • Choose Signal / Decoy / Vacuum
    • Set the corresponding mean photon number μ
    • Record the state selected

    Does NOT
    --------
    • Change wavelength
    • Change phase
    • Propagate through fiber
    """

    def __init__(

        self,

        signal_mu: float,

        decoy_mu: float,

        vacuum_mu: float,

        p_signal: float,

        p_decoy: float,

        p_vacuum: float,

        rng: np.random.Generator | None = None,

    ):

        self.signal_mu = signal_mu
        self.decoy_mu = decoy_mu
        self.vacuum_mu = vacuum_mu

        self.p_signal = p_signal
        self.p_decoy = p_decoy
        self.p_vacuum = p_vacuum

        self.rng = (

            np.random.default_rng()

            if rng is None

            else rng

        )

    # ---------------------------------------------------------

    def process(

        self,

        table: PulseTable,

    ) -> PulseTable:

        df = table.df

        n = len(df)

        r = self.rng.random(n)

        state = np.empty(n, dtype=object)

        mu = np.zeros(n)

        #
        # Signal
        #

        signal = r < self.p_signal

        state[signal] = "SIGNAL"

        mu[signal] = self.signal_mu

        #
        # Decoy
        #

        decoy = (

            (r >= self.p_signal)

            &

            (r < self.p_signal + self.p_decoy)

        )

        state[decoy] = "DECOY"

        mu[decoy] = self.decoy_mu

        #
        # Vacuum
        #

        vacuum = ~(signal | decoy)

        state[vacuum] = "VACUUM"

        mu[vacuum] = self.vacuum_mu

        #
        # Update pulse table
        #

        df["state"] = state

        df["mu"] = mu

        return table