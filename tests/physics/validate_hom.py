import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import config.experiment as EXP
from qkdengine.physics.hom import HOM

hom = HOM(

    eta_left=0.25,

    eta_right=0.25,

)

table = hom.process(

    "results/overlap.csv",

    "results/hom.csv",

)

print()

print("="*60)
print("WCP HOM VALIDATION")
print("="*60)

print()

print(

    table[

        [

            "alice_mu",
            "bob_mu",

            "left_intensity",
            "right_intensity",

            "left_click_probability",
            "right_click_probability",

            "coincidence_probability",

        ]

    ].head()

)

print()

print(

    table[

        [

            "coincidence_probability",

        ]

    ].describe()

)