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

from qkdengine.protocol.pair_builder import PairBuilder

print()

print("=" * 60)
print("PAIR BUILDER")
print("=" * 60)

builder = PairBuilder()

table = builder.process(

    "results/alice_fiber.csv",

    "results/bob_fiber.csv",

    "results/mode_pairs.csv",

    "results/paired_modes.csv",

)

print()

print(table)

print()

print("Pairs Built :", len(table))