import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 📂 Excel-Datei einlesen
fuellmengendatei = "fuellmengen_normal.xlsx"
df = pd.read_excel(fuellmengendatei)

# X̄- und R-Werte aus der Tabelle holen
X_bar = df["X̄"]
R = df["R"]
n = len(X_bar)  # Anzahl der Stichproben

# 🔢 Parameter für Kontrollgrenzen (typische Werte für n=5)
A2 = 0.577
D3 = 0
D4 = 2.114

# 🔍 Berechnung der Mittelwerte
X_double_bar = 500  # Zentrallinie muss 500 sein
R_bar = np.mean(R)  # Mittelwert der Spannweiten

# 📏 Berechnung der Kontrollgrenzen
UCL_X = X_double_bar + A2 * R_bar
LCL_X = X_double_bar - A2 * R_bar
UCL_R = D4 * R_bar
LCL_R = D3 * R_bar

# 📊 X̄-Karte plotten
plt.figure(figsize=(12, 6))
plt.axhline(X_double_bar, color="blue", linestyle="dotted", label="Mittelwert")
plt.axhline(UCL_X, color="red", linestyle="dashed", label="UCL")
plt.axhline(LCL_X, color="red", linestyle="dashed", label="LCL")
plt.plot(X_bar, marker="o", linestyle="-", label="X̄-Werte")
plt.legend()
plt.title("X̄-Karte mit Nelson-Regeln")
plt.xlabel("Stichprobe")
plt.ylabel("X̄-Wert")

# 📊 R-Karte plotten
plt.figure(figsize=(12, 6))
plt.axhline(UCL_R, color="red", linestyle="dashed", label="UCL")
plt.axhline(LCL_R, color="red", linestyle="dashed", label="LCL")
plt.axhline(R_bar, color="blue", linestyle="dotted", label="Mittelwert")
plt.plot(R, marker="o", linestyle="-", label="R-Werte")
plt.legend()
plt.title("R-Karte mit Nelson-Regeln")
plt.xlabel("Stichprobe")
plt.ylabel("R-Wert")
plt.show()

# Auswertungsdaten für Excel speichern
auswertung = []

# 📌 Nelson-Regeln für X̄-Karte prüfen und auswerten
for i in range(n):
    # Erstellen einer Zeile für jede Stichprobe
    auswertung_zeile = [i+1, X_bar[i], R[i]]

    # Regel 1: Punkt außerhalb der UCL oder LCL (X̄)
    rule_1_X = None
    if X_bar[i] > UCL_X or X_bar[i] < LCL_X:
        rule_1_X = "X"

    # Regel 2: 9 aufeinanderfolgende Punkte auf einer Seite des Mittelwerts (X̄)
    rule_2_X = None
    if i >= 8:
        if (all(X_bar[i-8:i+1] > X_double_bar) or all(X_bar[i-8:i+1] < X_double_bar)):
            rule_2_X = "X"

    # Regel 3: 6 aufeinanderfolgende Punkte steigen oder fallen (X̄)
    rule_3_X = None
    if i >= 5:
        if (all(X_bar[j] < X_bar[j+1] for j in range(i-5, i)) or all(X_bar[j] > X_bar[j+1] for j in range(i-5, i))):
            rule_3_X = "X"

    # Regel 4: 14 aufeinanderfolgende Punkte wechseln (Zick-Zack, X̄)
    rule_4_X = None
    if i >= 14:
        if all((X_bar[j] > X_bar[j-1] and X_bar[j] < X_bar[j+1]) or (X_bar[j] < X_bar[j-1] and X_bar[j] > X_bar[j+1]) for j in range(i-13, i)):
            rule_4_X = "X"

    # Regel 1: Punkt außerhalb der UCL oder LCL (R)
    rule_1_R = "X" if R[i] > UCL_R or R[i] < LCL_R else None

    # Regel 2: 9 aufeinanderfolgende Punkte auf einer Seite des Mittelwerts (R)
    rule_2_R = "X" if i >= 8 and (all(R[i-8:i+1] > R_bar) or all(R[i-8:i+1] < R_bar)) else None

    # Regel 3: 6 aufeinanderfolgende Punkte steigen oder fallen (R)
    rule_3_R = "X" if i >= 5 and (all(R[j] < R[j+1] for j in range(i-5, i)) or all(R[j] > R[j+1] for j in range(i-5, i))) else None

    # Regel 4: 14 aufeinanderfolgende Punkte wechseln (Zick-Zack, R)
    rule_4_R = "X" if i >= 14 and all((R[j] > R[j-1] and R[j] < R[j+1]) or (R[j] < R[j-1] and R[j] > R[j+1]) for j in range(i-13, i)) else None

    # Hinzufügen der Ergebnisse zur Auswertungs-Liste
    auswertung_zeile.extend([rule_1_X, rule_2_X, rule_3_X, rule_4_X, rule_1_R, rule_2_R, rule_3_R, rule_4_R])
    auswertung.append(auswertung_zeile)

# 🔄 Kopfzeile für Umwandlung der Auswertungsdaten in ein DataFrame
kopfzeile = [
    "Stichprobe", "X̄-Wert", "R-Wert", 
    "Regel 1 (X̄)", "Regel 2 (X̄)", "Regel 3 (X̄)", "Regel 4 (X̄)", 
    "Regel 1 (R)", "Regel 2 (R)", "Regel 3 (R)", "Regel 4 (R)"
]

# Umwandlung in DataFrame
df_auswertung = pd.DataFrame(auswertung, columns=kopfzeile)

# Auswertung in Datei speichern
auswertungsdatei = "prozessauswertung_normal.xlsx"

# 💾 Auswertung in eine Excel-Datei speichern
df_auswertung.to_excel(auswertungsdatei, index=False)
