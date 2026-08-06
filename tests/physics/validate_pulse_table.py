from qkdengine.recorder.pulse_table import PulseTable


table = PulseTable.create(

    1000,

)

print()

print("="*60)

print("PULSE TABLE")

print("="*60)

print()

print(table.df.head())

table.save(

    "results/pulse_table.csv",

)

print()

print("Saved.")

print()