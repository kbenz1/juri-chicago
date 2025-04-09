import pandas as pd
import random
from datetime import datetime, timedelta

# Funktion zum Generieren eines zufälligen Datums
def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

# Funktion zum Generieren zufälliger Beträge
def random_amount():
    return random.choice([50, 100, 500, 1000, 5000, 10000])

# Funktion zum Generieren zufälliger Beträge
def random_amount2():
    return random.choice([20, 110, 550, 900, 4000, 9000])


# Parameter
anzahl_transaktionen = 10000
zusatz_transaktionen = 5000  # Anzahl zusätzlicher zufälliger Transaktionen
start_date = datetime(2020, 1, 1)
end_date = datetime(2025, 1, 1)

# Listen zum Speichern der Daten
daten = []

# 1. Generierung der 10'000 gewünschten Transaktionen
for _ in range(anzahl_transaktionen):
    datum1 = random_date(start_date, end_date)
    datum2 = datum1 + timedelta(days=random.choice([-1, 0, 1]))  # Maximal 1 Tag auseinander
    betrag = random_amount()
    
    # Transaktion 1: Debitoren -> Umsatzerlöse
    daten.append({"Datum": datum1, "Soll": "Debitoren", "Haben": "Umsatzerlöse", "Betrag": betrag})
    
    # Transaktion 2: Kasse -> Darlehen
    daten.append({"Datum": datum2, "Soll": "Kasse", "Haben": "Darlehen", "Betrag": betrag})

# 2. Generierung zusätzlicher zufälliger Transaktionen
konten = ["Kasse", "Debitoren", "Kreditoren", "Umsatzerlöse", "Betriebsaufwand", "Darlehen"]
for _ in range(zusatz_transaktionen):
    datum = random_date(start_date, end_date)
    soll = random.choice(konten)
    haben = random.choice([konto for konto in konten if konto != soll])  # Kein Soll = Haben
    if soll == "Debitoren" and haben == "Umsatzerlöse":
        soll = "Kreditoren"
        haben = "Kasse"
    if soll == "Kasse" and haben == "Darlehen":
        soll = "Betriebsaufwand"
        haben = "Kasse"
    betrag = random_amount2()
    
    daten.append({"Datum": datum, "Soll": soll, "Haben": haben, "Betrag": betrag})

# DataFrame erstellen und nach Datum sortieren
df = pd.DataFrame(daten)
df.sort_values(by="Datum", inplace=True)

# Fortlaufende Nummer
df.insert(0, "Nr", range(1, len(df) + 1))

# Excel-Datei speichern
output_file = "buchungssaetze.xlsx"
df.to_excel(output_file, index=False)

print(f"Excel-Datei mit {len(daten)} Transaktionen wurde erstellt: {output_file}")
