import pandas as pd

# Excel-Datei einlesen
file_path = "buchungssaetze.xlsx"
df = pd.read_excel(file_path)

# df in Shell anzeigen
print(df)

# Annahme: Die Excel-Datei enthält folgende Spalten:
# - Nr
# - Datum (im Format DD.MM.YYYY)
# - Soll
# - Haben
# - Betrag

# Datumsformat anpassen und sortieren
df = df.sort_values(by="Datum")

buchungssaetze = df[df["Datum"] == "11.11.2021"]
print(buchungssaetze)


# Wir müssen nur Debitoren/Umsatzerlöse
# (Verkäufe auf Rechnung) anschauen
df_t1 = df[
    (df["Soll"] == "Debitoren")
    & (df["Haben"] == "Umsatzerlöse")]
print(df_t1)

# Suche nach Transaktionen, die die Kriterien erfüllen
# Liste der Treffer
transactions =  []

# Durch alle Verkäufe auf Rechnung durchgehen
for i, row1 in df_t1.iterrows():
    print(row1["Nr"])
    # Zeitfenster festlegen, nur +- 1 Tag
    min_date = row1["Datum"] - pd.Timedelta(days=1)
    max_date = row1["Datum"] + pd.Timedelta(days=1)

    
    # Nur Zeilen betrachten, die innerhalb
    # des Zeitfensters liegen
    # und Buchungen, die Kasse/Darlehen
    # (Kreditaufnahme) sind
    df_t2 = df[
        (df["Datum"] >= min_date)
        & (df["Datum"] <= max_date)
        & (df["Soll"] == "Kasse")
        & (df["Haben"] == "Darlehen")]

    # Durch diese Vergleichsbuchungen durchgehen
    for j, row2 in df_t2.iterrows():
        # Betrag der Vergleichsbuchung muss gleich sein
        # Und Vergleichsbuchung darf nicht
        # bereits als Trffer gespeichert sein
        if (
            row1["Betrag"] == row2["Betrag"]
            and row2["Nr"] not in transactions
            ):
            print(f"Neue Kreditaufnahme gefunden {row1['Nr']} {row2['Nr']}")
            # Anzahl bisherige Treffer
            n = len(transactions)
            print(f"Anzahl Kreditaufnahmen bisher: {n}")
            # Nummer der Transaktion hinzufügen
            transactions.append(row2["Nr"])
            break


# Ergebnisse ausgeben
if transactions:
    # Verdächtige Transaktionen wurden gefunden
    print("Verdächtige Transaktionen gefunden.")
    # Anzahl ausgeben
    n = len(transactions)
    print(f"Anzahl Transaktionen: {n}")
else:
    # Keine verdächtigen Transaktionen wurden gefunden
    print("Keine verdächtigen Transaktionen gefunden.")


