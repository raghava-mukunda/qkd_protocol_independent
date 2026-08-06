import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import config.experiment as EXP

from qkdengine.hardware.transmitter.laser import Laser
from qkdengine.hardware.transmitter.intensity_modulator import IntensityModulator
from qkdengine.hardware.transmitter.phase_modulator import PhaseModulator


laser = Laser(

    wavelength=EXP.LASER_WAVELENGTH,

    linewidth=EXP.LASER_LINEWIDTH,

    repetition_rate=EXP.LASER_REPETITION_RATE,

    output_power_dbm=EXP.LASER_POWER_DBM,

)

table = laser.generate(

    EXP.NUMBER_OF_PULSES,

)

im = IntensityModulator(

    signal_mu=EXP.SIGNAL_MU,

    decoy_mu=EXP.DECOY_MU,

    vacuum_mu=EXP.VACUUM_MU,

    p_signal=EXP.P_SIGNAL,

    p_decoy=EXP.P_DECOY,

    p_vacuum=EXP.P_VACUUM,

)

table = im.process(table)

pm = PhaseModulator()

table = pm.process(table)

table.save(

    "results/pm.csv"

)

print()

print("=" * 60)

print("PHASE MODULATOR")

print("=" * 60)

print()

print(

    table.df[
        [
            "pulse_id",
            "state",
            "mu",
            "phase",
        ]
    ].head()

)

print()

print("Phase Range")

print(

    table.df["phase"].min(),

    table.df["phase"].max(),

)