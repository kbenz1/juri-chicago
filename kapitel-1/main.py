import pandas as pd

# Excel-Datei einlesen
file_path = "buchhaltung.xlsx"
df = pd.read_excel(file_path)

# Annahme: Die Excel-Datei enthält folgende Spalten:
# - Datum (im Format YYYY-MM-DD oder DD.MM.YYYY)
# - Soll
# - Haben
# - Betrag

# Datumsformat anpassen und sortieren
df["Datum"] = pd.to_datetime(df["Datum"], day-first=True)
df.sort_values(by="Datum", inplace=True)

# Filterkriterien definieren
soll_konto_1 = "Debitoren"
haben_konto_1 = "Umsatzerlöse"
soll_konto_2 = "Kasse"
haben_konto_2 = "Darlehen"

# Suche nach Transaktionen, die die Kriterien erfüllen
matches = []
for i, row in df.iterrows():
    for j, compare_row in df.iterrows():
        if i != j:  # Keine Selbstvergleiche
            # Prüfen, ob die Beträge übereinstimmen
            if row["Betrag"] == compare_row["Betrag"]:
                # Prüfen, ob die Buchungskonten den Be-dingungen entsprechen
                if (
                    row["Soll"] == soll_konto_1
                    and row["Haben"] == haben_konto_1
                    and compare_row["Soll"] == soll_konto_2
                    and compare_row["Haben"] == ha-ben_konto_2
                ):
                    # Prüfen, ob die Transaktionen höchstens 1 Tag auseinanderliegen
                    if abs((row["Datum"] - com-pare_row["Datum"]).days) <= 1:
                        matches.append((row, com-pare_row))

# Ergebnisse ausgeben
if matches:
    print("Gefundene Transaktionen:")
    for match in matches:
        print("\n---")
        print("Transaktion 1:")
        print(match[0])
        print("Transaktion 2:")
        print(match[1])
else:
    print("Keine passenden Transaktionen gefunden.")
