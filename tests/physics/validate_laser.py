import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import config.experiment as EXP

from qkdengine.hardware.transmitter.laser import Laser


laser = Laser(

    wavelength=EXP.LASER_WAVELENGTH,

    linewidth=EXP.LASER_LINEWIDTH,

    repetition_rate=EXP.LASER_REPETITION_RATE,

    output_power_dbm=EXP.LASER_POWER_DBM,

)

table = laser.generate(

    EXP.NUMBER_OF_PULSES,

)

table.save(

    "results/laser.csv",

)

print()

print("=" * 60)

print("LASER VALIDATION")

print("=" * 60)

print()

print(table.df.head())

print()

print("Saved results/laser.csv")