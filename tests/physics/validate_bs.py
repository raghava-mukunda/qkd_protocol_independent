import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import config.experiment as EXP
from qkdengine.physics.beam_splitter import BeamSplitter
from qkdengine.recorder.pulse_table import PulseTable


alice = PulseTable.load(

    "results/alice_fiber.csv",

)

bob = PulseTable.load(

    "results/bob_fiber.csv",

)

bs = BeamSplitter()

alice, bob = bs.process(

    alice,

    bob,

)

alice.save(

    "results/alice_bs.csv",

)

bob.save(

    "results/bob_bs.csv",

)

print()

print("=" * 60)

print("BEAM SPLITTER")

print("=" * 60)

print()

print(

    alice.df[
        [
            "mu",
            "phase",
            "left_intensity",
            "right_intensity",
        ]
    ].head()

)