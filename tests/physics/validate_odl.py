import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import config.experiment as EXP
from qkdengine.hardware.channel.optical_delay_line import OpticalDelayLine
from qkdengine.recorder.pulse_table import PulseTable


print()

print("=" * 60)

print("OPTICAL DELAY LINE VALIDATION")

print("=" * 60)

#
# Load Alice and Bob after fiber propagation
#

alice = PulseTable.load(

    "results/alice_fiber.csv",

)

bob = PulseTable.load(

    "results/bob_fiber.csv",

)

#
# Apply ODL
#

odl = OpticalDelayLine(

    delay=EXP.ODL_DELAY,

)

alice, bob = odl.process(

    alice,

    bob,

)

#
# Save updated tables
#

alice.save(

    "results/alice_odl.csv",

)

bob.save(

    "results/bob_odl.csv",

)

print()

print(

    bob.df[
        [
            "arrival_time",
            "timing_error_before",
            "timing_error_after",
        ]
    ].head()

)

print()

print(

    "Mean timing error before (ps):",

    bob.df["timing_error_before"].mean() * 1e12,

)

print(

    "Mean timing error after (ps):",

    bob.df["timing_error_after"].mean() * 1e12,

)

print()

print(

    "Maximum residual timing error (ps):",

    bob.df["timing_error_after"].abs().max() * 1e12,

)