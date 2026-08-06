import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import config.experiment as EXP

from qkdengine.hardware.transmitter.laser import Laser
from qkdengine.hardware.transmitter.intensity_modulator import IntensityModulator
from qkdengine.hardware.transmitter.phase_modulator import PhaseModulator
from qkdengine.hardware.transmitter.voa import VariableOpticalAttenuator
from qkdengine.hardware.channel.fiber import Fiber


laser = Laser(

    wavelength=EXP.LASER_WAVELENGTH,

    linewidth=EXP.LASER_LINEWIDTH,

    repetition_rate=EXP.LASER_REPETITION_RATE,

    output_power_dbm=EXP.LASER_POWER_DBM,

)

table = laser.generate(

    EXP.NUMBER_OF_PULSES,

)

table = IntensityModulator(

    signal_mu=EXP.SIGNAL_MU,

    decoy_mu=EXP.DECOY_MU,

    vacuum_mu=EXP.VACUUM_MU,

    p_signal=EXP.P_SIGNAL,

    p_decoy=EXP.P_DECOY,

    p_vacuum=EXP.P_VACUUM,

).process(table)

table = PhaseModulator().process(table)

table = VariableOpticalAttenuator(

    attenuation_db=EXP.VOA_ATTENUATION_DB,

).process(table)

fiber = Fiber(

    length_km=EXP.FIBER_LENGTH_KM,

    attenuation_db_per_km=EXP.FIBER_ATTENUATION_DB_PER_KM,

    refractive_index=EXP.FIBER_REFRACTIVE_INDEX,

    phase_noise_std=EXP.FIBER_PHASE_NOISE_STD,

    polarization_std=EXP.FIBER_POLARIZATION_STD,

)

table = fiber.process(table)

table.save(

    "results/fiber.csv",

)

print()

print("=" * 60)

print("FIBER VALIDATION")

print("=" * 60)

print()

print(

    table.df[
        [
            "mu",
            "arrival_time",
            "phase",
            "polarization_x",
            "polarization_y",
        ]
    ].head()

)

print()

print(

    "Transmission :",

    fiber.transmission,

)

print(

    "Delay (µs) :",

    fiber.propagation_delay * 1e6,

)