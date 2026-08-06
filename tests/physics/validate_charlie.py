import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import config.experiment as EXP
from qkdengine.relay.charlie import Charlie
from qkdengine.recorder.pulse_table import PulseTable

table = PulseTable.load(

    "results/alice_detector.csv",

)

charlie = Charlie()

table = charlie.process(

    table,

)

table.save(

    "results/charlie.csv",

)

print()

print("=" * 60)
print("CHARLIE VALIDATION")
print("=" * 60)

print()

print(

    table.df[

        [

            "left_click",

            "right_click",

            "detector",

            "bell_state",

            "bell_success",

        ]

    ].head(20)

)

print()

print(

    table.df["detector"].value_counts()

)

print()

print(

    "Bell Success =",

    table.df["bell_success"].sum(),

)