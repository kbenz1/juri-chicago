import pandas as pd
from scipy.stats import chi2_contingency

# Datei einlesen (Excel-Datei mit Daten der zwei Gruppen)
input_file = "daten.xlsx"  # Passe den Dateinamen an
output_file = "ergebnisse.xlsx"

# Daten aus der Excel-Tabelle lesen
df = pd.read_excel(input_file)

# Kreuztabelle erstellen
cross_tab = pd.crosstab(df['Gruppe'], df['Diagnose'])

# Entferne die Wörter "Gruppe" und "Diagnose"
cross_tab.index.name = None
cross_tab.columns.name = None

print(cross_tab)

# Chi-Quadrat-Test durchführen
chi2, p, fre_grad, expected = chi2_contingency(cross_tab)

# Erwartete Ergebnisse
expected_df = pd.DataFrame(expected, index=cross_tab.index, columns=cross_tab.columns)

# Zahlen auf null Kommastellen runden.
expected_df = expected_df.round(0)

print(expected_df)

# Ergebnisse formatieren
chi_square_results = {
    "Chi-Quadrat-Wert": [chi2],
    "Erreichtes Signifikanzniveau": [p if p >= 0.05 else "< 5%"],
    "Freiheitsgrade": [fre_grad],
    "Zusammenhang gefunden?": ["Nein" if p >= 0.05 else "Ja"]
}
results = pd.DataFrame(chi_square_results)

# Zahlen auf 4 Kommastellen runden.
results = results.round(4)

print(results)

# Ergebnisse in ein Excel schreiben
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    cross_tab.to_excel(writer, sheet_name="Kreuztabelle")
    expected_df.to_excel(writer, sheet_name="Erwartete Werte")
    results.to_excel(writer, sheet_name="Chi-Quadrat-Ergebnisse", index=False)

print(f"Die Ergebnisse wurden erfolgreich in '{output_file}' gespeichert.")
