import pandas as pd
import numpy as np
import random

np.random.seed(42)

# Bausteine für Namen
vorname_us = ["Walker", "Anderson", "Carter", "Miller", "Jackson", "Hunter", "Smith", "Cooper",
              "Johnson", "Hamilton", "Clark", "Wesley", "Winston", "Black", "Brown"]
vorname_jp = ["Yamamoto", "Takahashi", "Tanaka", "Sato", "Shimizu", "Fujimoto", "Kobayashi", "Matsuda"]

branchen = [
    "Auto", "Bau", "Solar", "Tech", "Robotics", "Logistics", "Textiles", "Energy", "Foods", "Motors", "IT", "AI", "Wholesale"
]

rechtsformen = ["AG", "GmbH", "GmbH & Co. KG"]

# Set für eindeutige Namen
verwendete_namen = set()

def generiere_firmenname():
    while True:
        stil = random.choice(["us", "jp"])
        name = random.choice(vorname_us if stil == "us" else vorname_jp)
        branche = random.choice(branchen)
        rechtsform = random.choice(rechtsformen)
        firmenname = f"{name} {branche} {rechtsform}"

        if firmenname not in verwendete_namen:
            verwendete_namen.add(firmenname)
            return firmenname

# Anzahl Firmen
anzahl = 100

# Zufallswerte generieren
einkommen = np.random.normal(100_000, 40_000, anzahl).clip(10_000)
vermoegen = np.random.normal(300_000, 150_000, anzahl).clip(0)
gold = np.random.normal(30, 15, anzahl).clip(0)
immobilien = np.random.normal(200_000, 100_000, anzahl).clip(0)

# Auf gewünschte Genauigkeit runden
einkommen = np.round(einkommen, -3)
vermoegen = np.round(vermoegen, -3)
gold = np.round(gold, -1)
immobilien = np.round(immobilien, -3)

# DataFrame erstellen
daten = {
    "Name": [generiere_firmenname() for _ in range(anzahl)],
    "Einkommen": einkommen,
    "Vermögen": vermoegen,
    "Gold": gold,
    "Immobilien": immobilien,
}

df = pd.DataFrame(daten)

# Gruppeneinteilung
def bestimme_gruppe(e, v, g, immo):
    punkte = 0
    if e > 120_000: punkte += 1
    if v > 400_000: punkte += 1
    if g > 50:      punkte += 1
    if immo > 300_000: punkte += 1

    if punkte >= 3:
        return "A"
    elif punkte == 2:
        return "B"
    else:
        return "C"

df["Gruppe"] = df.apply(lambda row: bestimme_gruppe(row["Einkommen"], row["Vermögen"], row["Gold"], row["Immobilien"]), axis=1)

# Excel speichern
dateiname = "kreditnehmerinnen.xlsx"
df.to_excel(dateiname, index=False)
print(f"✅ Excel-Datei '{dateiname}' wurde erfolgreich mit einzigartigen japanisch/amerikanischen Firmennamen erstellt.")
