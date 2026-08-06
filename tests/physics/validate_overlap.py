import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import config.experiment as EXP
from qkdengine.physics.overlap import Overlap


overlap = Overlap()

table = overlap.process(

    "results/alice_fiber.csv",

    "results/bob_fiber.csv",

    "results/overlap.csv",

)

print()

print("=" * 60)
print("OVERLAP VALIDATION")
print("=" * 60)

print()

print(table.head())

print()

print(table.describe())