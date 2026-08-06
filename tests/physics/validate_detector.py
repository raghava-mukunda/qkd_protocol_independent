import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import config.experiment as EXP

from qkdengine.detector.snspd import SNSPD
from qkdengine.recorder.pulse_table import PulseTable

table = PulseTable.load(

    "results/alice_bs.csv",

)

detector = SNSPD(

    efficiency=EXP.SNSPD_EFFICIENCY,

)

table = detector.process(

    table,

)

table.save(

    "results/alice_detector.csv",

)

print()

print("=" * 60)
print("SNSPD VALIDATION")
print("=" * 60)

print(

    table.df[

        [

            "left_intensity",

            "right_intensity",

            "left_click_probability",

            "right_click_probability",

            "left_click",

            "right_click",

        ]

    ].head()

)

print()

print(

    "Left Clicks :",

    table.df["left_click"].sum(),

)

print(

    "Right Clicks:",

    table.df["right_click"].sum(),

)