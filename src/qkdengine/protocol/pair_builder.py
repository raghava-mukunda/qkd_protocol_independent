from __future__ import annotations

import pandas as pd


class PairBuilder:
    """
    Builds logical MP-QKD data pairs.

    Inputs
    ------
    alice.csv
    bob.csv
    mode_pairs.csv

    Output
    ------
    paired_modes.csv
    """

    def process(

        self,

        alice_csv,
        bob_csv,
        pairs_csv,
        output_csv,

    ):

        alice = pd.read_csv(alice_csv)
        bob = pd.read_csv(bob_csv)
        pairs = pd.read_csv(pairs_csv)

        rows = []

        for _, pair in pairs.iterrows():

            i = int(pair["pulse_i"])
            j = int(pair["pulse_j"])

            Ai = alice.iloc[i]
            Aj = alice.iloc[j]

            Bi = bob.iloc[i]
            Bj = bob.iloc[j]

            rows.append(

                {

                    #
                    # Pair information
                    #

                    "pair_id": pair["pair_id"],
                    "pulse_i": i,
                    "pulse_j": j,

                    #
                    # Alice
                    #

                    "alice_state_i": Ai["state"],
                    "alice_state_j": Aj["state"],

                    "alice_mu_i": Ai["mu"],
                    "alice_mu_j": Aj["mu"],

                    "alice_phase_i": Ai["phase"],
                    "alice_phase_j": Aj["phase"],

                    #
                    # Bob
                    #

                    "bob_state_i": Bi["state"],
                    "bob_state_j": Bj["state"],

                    "bob_mu_i": Bi["mu"],
                    "bob_mu_j": Bj["mu"],

                    "bob_phase_i": Bi["phase"],
                    "bob_phase_j": Bj["phase"],

                    #
                    # Charlie
                    #

                    "detector_i": pair["detector_i"],
                    "detector_j": pair["detector_j"],

                    "bell_i": pair["bell_i"],
                    "bell_j": pair["bell_j"],

                    #
                    # Empty protocol fields
                    #

                    "alice_basis": "",
                    "bob_basis": "",
                    "protocol_use": "",
                    #"keep_pair": False,

                }

            )

        paired = pd.DataFrame(rows)

        paired.to_csv(

            output_csv,

            index=False,

        )

        return paired