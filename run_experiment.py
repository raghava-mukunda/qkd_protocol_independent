from pathlib import Path
import subprocess
import sys

pipeline = [

    "tests/physics/validate_alice_bob_fiber.py",

    "tests/physics/validate_odl.py",

    "tests/physics/validate_overlap.py",

    "tests/physics/validate_bs.py",

    "tests/physics/validate_detector.py",

    "tests/physics/validate_charlie.py",

    "tests/physics/validate_mode.py",

    "tests/physics/validate_pair_builder.py",

    "tests/physics/validate_basis_sifting.py",

]

print()
print("=" * 80)
print("MP-QKD DIGITAL TWIN")
print("=" * 80)

print()
print("Pipeline")
print("-" * 80)

for i, script in enumerate(pipeline, start=1):

    print(f"{i}. {Path(script).stem}")

print()

#
# Run pipeline
#

for script in pipeline:

    print()
    print("=" * 80)
    print(f"Running : {Path(script).stem}")
    print("=" * 80)

    result = subprocess.run(

        [sys.executable, script]

    )

    if result.returncode != 0:

        print()
        print("FAILED :", script)

        break

print()

print("=" * 80)
print("SIMULATION COMPLETE")
print("=" * 80)