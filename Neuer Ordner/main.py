import pandas as pd
from scipy.stats import chi2_contingency

# Datei einlesen (Excel-Datei mit Daten der zwei Gruppen)
input_file = "daten.xlsx"  # Passe den Dateinamen an
output_file = "ergebnisse.xlsx"

# Daten aus der Excel-Tabelle lesen
df = pd.read_excel(input_file)

# Kreuztabelle erstellen
cross_tab = pd.crosstab(df['Upround?'], df['Schwipps?'])

# Chi-Quadrat-Test durchführen
chi2, p, dof, expected = chi2_contingency(cross_tab)

# Ergebnisse formatieren
chi_square_results = {
    "Chi-Quadrat-Wert": [chi2],
    "p-Wert": [p],
    "Freiheitsgrade": [dof]
}
expected_df = pd.DataFrame(expected, index=cross_tab.index, columns=cross_tab.columns)

# Ergebnisse in ein Excel schreiben
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    cross_tab.to_excel(writer, sheet_name="Kreuztabelle")
    pd.DataFrame(chi_square_results).to_excel(writer, sheet_name="Chi-Quadrat-Ergebnisse")
    expected_df.to_excel(writer, sheet_name="Erwartete Werte")

print(f"Die Ergebnisse wurden erfolgreich in '{output_file}' gespeichert.")
