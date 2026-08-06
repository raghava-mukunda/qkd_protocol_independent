from __future__ import annotations

from pathlib import Path
import pandas as pd


class PulseTable:
    """
    Master Pulse Table

    One row = one transmitted optical pulse.

    Every hardware block updates this table.
    """

    def __init__(

        self,

        dataframe: pd.DataFrame,

    ):

        self.df = dataframe

    # =========================================================

    @classmethod
    def create(

        cls,

        number_of_pulses: int,

    ):

        df = pd.DataFrame(

            {

                # =================================================
                # Identification
                # =================================================

                "pulse_id": range(number_of_pulses),

                "timestamp": 0.0,

                # =================================================
                # Laser
                # =================================================

                "wavelength": 0.0,

                "linewidth": 0.0,

                "power_dbm": 0.0,

                # =================================================
                # State Preparation
                # =================================================

                "state": "",

                "mu": 0.0,

                "phase": 0.0,

                "polarization_x": 1.0,

                "polarization_y": 0.0,

                # =================================================
                # Fiber Channel
                # =================================================

                "transmission": 1.0,

                "arrival_time": 0.0,

                "frequency_shift": 0.0,

                "timing_jitter": 0.0,

                "phase_noise": 0.0,

                "polarization_rotation": 0.0,

                # =================================================
                # Overlap
                # =================================================

                "temporal_overlap": 0.0,

                "spectral_overlap": 0.0,

                "polarization_overlap": 0.0,

                "total_overlap": 0.0,

                # =================================================
                # Beam Splitter
                # =================================================

                "left_intensity": 0.0,

                "right_intensity": 0.0,

                # =================================================
                # SNSPD
                # =================================================

                "left_click_probability": 0.0,

                "right_click_probability": 0.0,

                "left_click": False,

                "right_click": False,

                # =================================================
                # Charlie
                # =================================================

                "detector": "",

                "bell_state": "",

                "bell_success": False,

            }

        )

        return cls(df)

    # =========================================================

    def save(

        self,

        filename,

    ):

        Path(filename).parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        self.df.to_csv(

            filename,

            index=False,

        )

    # =========================================================

    @classmethod
    def load(

        cls,

        filename,

    ):

        return cls(

            pd.read_csv(

                filename,

            )

        )