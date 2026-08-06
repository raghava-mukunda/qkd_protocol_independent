from __future__ import annotations

from qkdengine.recorder.pulse_table import PulseTable


class VariableOpticalAttenuator:
    """
    Electronic Variable Optical Attenuator (VOA).

    Applies a fixed attenuation to every pulse.

    The attenuation is specified in dB.

    μ_out = μ_in × 10^(-Loss/10)
    """

    def __init__(

        self,

        attenuation_db: float,

    ):

        self.attenuation_db = attenuation_db

    # ---------------------------------------------------------

    @property
    def transmission(self):

        return 10 ** (

            -self.attenuation_db

            / 10

        )

    # ---------------------------------------------------------

    def process(

        self,

        table: PulseTable,

    ) -> PulseTable:

        df = table.df

        df["mu"] *= self.transmission

        df["power_dbm"] -= self.attenuation_db

        return table