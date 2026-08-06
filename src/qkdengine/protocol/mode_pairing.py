from __future__ import annotations

import pandas as pd


class ModePairing:
    """
    MP-QKD Mode Pairing

    Implements Box 2 from the paper.

    Input
    -----
    charlie.csv

    Output
    ------
    mode_pairs.csv

    Only creates logical pairs.
    """

    def __init__(

        self,

        pairing_window: int = 100,

    ):

        self.pairing_window = pairing_window

    # ------------------------------------------------------------

    def process(

        self,

        charlie_csv,

        output_csv,

    ):

        table = pd.read_csv(charlie_csv)

        #
        # Keep only successful BSM events
        #
        success = table[
            table["bell_success"] == True
        ].copy()

        success = success.sort_values(
            "pulse_id"
        ).reset_index(drop=True)

        pairs = []

        flag = False
        front = None
        pair_id = 0

        #
        # Box 2 algorithm
        #

        for _, row in success.iterrows():

            if not flag:

                front = row
                flag = True
                continue

            distance = (
                int(row["pulse_id"])
                -
                int(front["pulse_id"])
            )

            #
            # Within pairing window
            #

            if distance <= self.pairing_window:

                pairs.append(

                    {

                        "pair_id": pair_id,

                        #
                        # paired rounds
                        #

                        "pulse_i": int(front["pulse_id"]),
                        "pulse_j": int(row["pulse_id"]),

                        #
                        # separation
                        #

                        "pair_distance": distance,

                        #
                        # Charlie announcement
                        #

                        "detector_i": front["detector"],
                        "detector_j": row["detector"],

                        "bell_i": front["bell_state"],
                        "bell_j": row["bell_state"],

                    }

                )

                pair_id += 1

                flag = False

            else:

                #
                # previous front discarded
                # current becomes new front
                #

                front = row
                flag = True

        pairs = pd.DataFrame(pairs)

        pairs.to_csv(

            output_csv,

            index=False,

        )

        return pairs