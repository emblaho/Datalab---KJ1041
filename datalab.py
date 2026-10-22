
import pyscf

#lager et molekylobjekt med startgeomerien og6-311+G* og AO-basissett
molekyl = pyscf.M(
    atom="co2_start.xyz",
    unit="Angstrom",
    basis="6-311+G*",
    charge=0,
    spin=0
)

print("Antall atomer:", molekyl.natm)
print("Antall elektroner:", molekyl.nelectron)

from pyscf.geomopt.geometric_solver import optimize

# Opprett en Hartree–Fock-beregning
hf = molekyl.HF()

#Juster atomplasseringene for å minimere energien
optimalisert = optimize(hf, maxsteps=50)

#Lagre den nye geometrien i en egen xyz-fil
optimalisert.tofile("co2_opt.xyz", format="xyz")

print("Optimalisert geometri:")
print(optimalisert.tostring(format="xyz"))