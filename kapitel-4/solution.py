import pandas as pd
from scipy.stats import chi2_contingency

# Dateinamen bestimmen für Daten von Testpersonen und Ergebnisse
input_file = "daten.xlsx"
output_file = "ergebnisse.xlsx"

# Daten aus "daten.xlsx" einlesen
df = pd.read_excel(input_file)

print(df)

# Kreuztabelle erstellen
cross_tab = pd.crosstab(df['Gruppe'], df['Diagnose'])

print(cross_tab)

# Entferne die Wörter aus linker oberer Ecke
cross_tab.index.name = None
cross_tab.columns.name = None

print(cross_tab)

# Chi-Quadrat-Test durchführen
chi2, p, fre_grad, expected = chi2_contingency(cross_tab)

# Kreuztabelle mit erwarteten Ergebnissen bilden
expected_df = pd.DataFrame(expected, index=cross_tab.index, columns=cross_tab.columns)

print(expected_df)

# Zahlen auf null Kommastellen runden.
expected_df = expected_df.round(0)

print(expected_df)

# Ergebnisse formatieren
chi_square_results = {
    "Chi-Quadrat": [chi2],
    "p-Wert": [p if p >= 0.05 else "< 5%"],
    "Freiheitsgrade": [fre_grad],
    "Zusammenhang gefunden?": ["Nein" if p >= 0.05 else "Ja"]
}
results = pd.DataFrame(chi_square_results)

print(results)

# Zahlen auf 2 Kommastellen runden.
results = results.round(2)

print(results)

# Ergebnisse in ein Excel schreiben
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    cross_tab.to_excel(writer, sheet_name="Kreuztabelle")
    expected_df.to_excel(writer, sheet_name="Erwartete Werte")
    results.to_excel(writer, sheet_name="Chi-Quadrat-Ergebnisse", index=False)

print(f"Die Ergebnisse wurden erfolgreich in '{output_file}' gespeichert.")
