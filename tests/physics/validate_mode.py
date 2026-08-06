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

from qkdengine.protocol.mode_pairing import ModePairing

print()

print("=" * 60)
print("MODE PAIRING")
print("=" * 60)

pairing = ModePairing(

    pairing_window=EXP.PAIRING_WINDOW,

)

pairs = pairing.process(

    "results/charlie.csv",

    "results/mode_pairs.csv",

)

print()

print(pairs)

print()

print(

    "Number of pairs:",

    len(pairs),

)