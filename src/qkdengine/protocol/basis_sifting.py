from __future__ import annotations

import pandas as pd


class BasisSifting:
    """
    MP-QKD Basis Sifting.

    Determines the preparation basis
    from Alice's and Bob's prepared states.

    Basis
    -----
    Z
    X
    DECOY
    INVALID

    Also assigns protocol usage

    KEY
    DECOY
    DISCARD
    """

    # ---------------------------------------------------------

    def determine_basis(

        self,

        state_i,
        state_j,

    ):

        #
        # Signal-Vacuum
        #

        if (

            state_i == "SIGNAL"

            and

            state_j == "VACUUM"

        ):

            return "Z"

        #
        # Vacuum-Signal
        #

        if (

            state_i == "VACUUM"

            and

            state_j == "SIGNAL"

        ):

            return "Z"

        #
        # Signal-Signal
        #

        if (

            state_i == "SIGNAL"

            and

            state_j == "SIGNAL"

        ):

            return "X"

        #
        # Any decoy

        #

        if (

            state_i == "DECOY"

            or

            state_j == "DECOY"

        ):

            return "DECOY"

        #
        # Vacuum-Vacuum

        #

        return "INVALID"

    # ---------------------------------------------------------

    def process(

        self,

        input_csv,
        output_csv,

    ):

        table = pd.read_csv(

            input_csv,

        )

        alice_basis = []
        bob_basis = []
        protocol_use = []

        for _, row in table.iterrows():

            A = self.determine_basis(

                row["alice_state_i"],
                row["alice_state_j"],

            )

            B = self.determine_basis(

                row["bob_state_i"],
                row["bob_state_j"],

            )

            alice_basis.append(A)
            bob_basis.append(B)

            #
            # Decide protocol usage
            #

            if A == "DECOY" or B == "DECOY":

                protocol_use.append("DECOY")

            elif (

                A == B

                and

                A in [

                    "X",

                    "Z",

                ]

            ):

                protocol_use.append("KEY")

            else:

                protocol_use.append("DISCARD")

        table["alice_basis"] = alice_basis
        table["bob_basis"] = bob_basis
        table["protocol_use"] = protocol_use

        table.to_csv(

            output_csv,

            index=False,

        )

        return table