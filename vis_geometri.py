import numpy as np
import matplotlib.pyplot as plt


# Les atomnavn og koordinater fra en xyz-fil
def les_xyz(filnavn):
    with open(filnavn) as fil:
        linjer = fil.readlines()

    antall = int(linjer[0])
    atomer = []
    koordinater = []

    for linje in linjer[2:2 + antall]:
        deler = linje.split()
        atomer.append(deler[0])
        koordinater.append(
            [float(verdi) for verdi in deler[1:4]]
        )

    return atomer, np.array(koordinater)


# Geometrifiler som skal leses, og bilder som skal lagres
geometrier = [
    ("co2_start.xyz", "Før optimalisering", "co2_for.png"),
    ("co2_opt.xyz", "Etter optimalisering", "co2_etter.png")
]


for filnavn, tittel, bildefil in geometrier:
    atomer, koordinater = les_xyz(filnavn)

    karbon = atomer.index("C")
    oksygen = [
        i for i, atom in enumerate(atomer) if atom == "O"
    ]

    # Beregn vektorer fra karbon til hvert oksygen
    v1 = koordinater[oksygen[0]] - koordinater[karbon]
    v2 = koordinater[oksygen[1]] - koordinater[karbon]

    # Beregn bindingslengder
    r1 = np.linalg.norm(v1)
    r2 = np.linalg.norm(v2)

    # Beregn bindingsvinkel
    cos_vinkel = np.dot(v1, v2) / (r1 * r2)
    vinkel = np.degrees(
        np.arccos(np.clip(cos_vinkel, -1, 1))
    )

    # Skriv resultatene i terminalen
    print(f"\n{tittel}")
    print(f"C–O1-avstand: {r1:.8f} Å")
    print(f"C–O2-avstand: {r2:.8f} Å")
    print(f"O–C–O-vinkel: {vinkel:.2f} grader")

    print("\nXYZ-koordinater i Å:")
    print("Atom          x            y            z")

    for i, (atom, (x, y, z)) in enumerate(
        zip(atomer, koordinater)
    ):
        if atom == "C":
            navn = "C"
        else:
            navn = f"O{oksygen.index(i) + 1}"

        print(f"{navn:4s} {x:12.8f} {y:12.8f} {z:12.8f}")

    # Lag en egen figur for denne geometrien
    fig, akse = plt.subplots(figsize=(5, 3))

    # Tegn bindingene og skriv bindingslengdene
    for i in oksygen:
        akse.plot(
            [koordinater[karbon, 2], koordinater[i, 2]],
            [koordinater[karbon, 0], koordinater[i, 0]],
            color="black",
            linewidth=3,
            zorder=1
        )

        avstand = np.linalg.norm(
            koordinater[i] - koordinater[karbon]
        )

        midtpunkt = (
            koordinater[karbon, 2] + koordinater[i, 2]
        ) / 2

        akse.text(
            midtpunkt,
            koordinater[karbon, 0] + 0.25,
            f"{avstand:.3f} Å",
            ha="center"
        )

    # Tegn atomene, med z-aksen vannrett
    for i, (atom, (x, y, z)) in enumerate(
        zip(atomer, koordinater)
    ):
        farge = "dimgray" if atom == "C" else "firebrick"

        if atom == "C":
            navn = "C"
        else:
            navn = f"O{oksygen.index(i) + 1}"

        akse.scatter(
            z, x, s=850, color=farge, zorder=2
        )

        akse.text(
            z, x, navn,
            color="white",
            ha="center",
            va="center",
            fontweight="bold",
            zorder=3
        )

    akse.set_title(tittel)
    akse.set_xlim(-1.7, 1.7)
    akse.set_ylim(-0.6, 0.6)
    akse.set_aspect("equal")
    akse.axis("off")

    fig.tight_layout()
    fig.savefig(bildefil, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"\nBilde lagret: {bildefil}")