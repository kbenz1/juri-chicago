import pickle
import pandas as pd

# Entscheidungsbaum laden
with open("baummodell.pkl", "rb") as f:
    clf = pickle.load(f)

# Neue Daten einlesen
df_neu = pd.read_excel("kredite_greenwash2025.xlsx")

# Vorverarbeitung wie beim Training
features = ['Umsatz', 'Vermögen', 'Gold', 'Immobilien']
for feat in features:
    df_neu[feat + '_cat'] = pd.qcut(df_neu[feat], 3, labels=[0, 1, 2]).astype(int)

X_neu = df_neu[[feat + '_cat' for feat in features]]

# Klassifikation mit gespeichertem Baum
y_pred = clf.predict(X_neu)

# Ergebnis hinzufügen
df_neu["vorh_Gruppe"] = y_pred

# Ergebnis anzeigen
print(df_neu[["Name", "vorh_Gruppe"]])

# Ergebnis speichern
df_neu.to_excel("korrekte_kredite_greenwash2025.xlsx", index=False)
