import pyscf

# Les den optimaliserte geometrien med minimal basis
molekyl = pyscf.M(
    atom="co2_opt.xyz",
    unit="Angstrom",
    basis="sto-3g",
    charge=0,
    spin=0
)

# Kjør en Hartree–Fock-beregning
hf = molekyl.HF()
hf.run()

# Sjekk om beregningen har konvergert
if not hf.converged:
    raise RuntimeError("Beregningen konvergerte ikke.")

# Skriv ut molekylets totalenergi
print("\nHartree–Fock-totalenergi:")
print(f"{hf.e_tot:.10f} Hartree")

# Skriv ut energien og antall elektroner i hver MO
print("\nMO     Energi (Hartree)     Antall elektroner")

for nummer, (energi, antall) in enumerate(
    zip(hf.mo_energy, hf.mo_occ), start=1
):
    print(f"{nummer:2d}     {energi: .8f}          {antall:.0f}")