import pandas as pd

# Excel-Datei einlesen
file_path = "buchungssaetze.xlsx"
df = pd.read_excel(file_path)

# Annahme: Die Excel-Datei enthält folgende Spalten:
# - Nr
# - Datum (im Format YYYY-MM-DD oder DD.MM.YYYY)
# - Soll
# - Haben
# - Betrag

# Datumsformat anpassen und sortieren
df["Datum"] = pd.to_datetime(df["Datum"], dayfirst=True)
df.sort_values(by="Datum", inplace=True)

# Filterkriterien definieren
soll_konto_1 = "Debitoren"
haben_konto_1 = "Umsatzerlöse"
soll_konto_2 = "Kasse"
haben_konto_2 = "Darlehen"

# Suche nach Transaktionen, die die Kriterien erfüllen
# Liste der Treffer
matches =  []

# Wir müssen nur Debitoren/Umsatzerlöse
# (Verkäufe auf Rechnung) anschauen
df_t1 = df[
    (df["Soll"] == soll_konto_1)
    & (df["Haben"] == haben_konto_1)]

# Durch alle Verkäufe auf Rechnung durchgehen
for i, row1 in df_t1.iterrows():

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
        & (df["Soll"] == soll_konto_2)
        & (df["Haben"] == haben_konto_2)]

    # Durch diese Vergleichsbuchungen durchgehen
    for j, row2 in df_t2.iterrows():
        # Betrag der Vergleichsbuchung muss gleich sein
        # Und Vergleichsbuchung darf nicht
        # bereits als Trffer gespeichert sein
        if (
            row1["Betrag"] == row2["Betrag"]
            and row2["Nr"] not in matches
            ):
            print("Neue Kreditaufnahme gefunden")
            # Anzahl bisherige Treffer
            n = len(matches)
            print(f"Anzahl Kreditaufnahmen bisher: {n}")
            # Nummer der Transaktion hinzufügen
            matches.append(row2["Nr"])


# Ergebnisse ausgeben
if matches:
    # Verdächtige Transaktionen wurden gefunden
    print("Verdächtige Transaktionen gefunden.")
    # Anzahl ausgeben
    n = len(matches)
    print(f"Anzahl Transaktionen: {n}")
else:
    # Keine verdächtigen Transaktionen wurden gefunden
    print("Keine verdächtigen Transaktionen gefunden.")

