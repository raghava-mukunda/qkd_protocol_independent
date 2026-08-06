import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import config.experiment as EXP
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(

    0,

    str(ROOT / "src"),

)

from qkdengine.protocol.basis_sifting import BasisSifting

print()

print("=" * 60)
print("BASIS SIFTING")
print("=" * 60)

basis = BasisSifting()

table = basis.process(

    "results/paired_modes.csv",

    "results/paired_modes.csv",

)

print()

print(

    table[

        [

            "pair_id",

            "alice_state_i",
            "alice_state_j",

            "bob_state_i",
            "bob_state_j",

            "alice_basis",
            "bob_basis",

            "protocol_use",

        ]

    ]

)

print()

print(

    table["protocol_use"].value_counts()

)