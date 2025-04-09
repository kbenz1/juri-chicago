import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 📂 Excel-Datei einlesen
fuellmengendatei = "fuellmengen_fillfix.xlsx"
auswertungsatei = "prozessauswertung_fillfix.xlsx"
df = pd.read_excel(fuellmengendatei)

# X̄- und R-Werte aus der Tabelle holen
X_bar = df["X̄"]
R = df["R"]
n = len(X_bar)  # Anzahl der Stichproben

# 🔢 Parameter für Kontrollgrenzen (typische Werte für n=5)
A2, D3, D4 = 0.577, 0, 2.114

# 🔍 Berechnung der Mittelwerte
X_double_bar = 500  # Zentrallinie muss 500 sein
R_bar = np.mean(R)  # Mittelwert der Spannweiten

# 📏 Berechnung der Eingriffsgrenzen
UCL_X = X_double_bar + A2 * R_bar
LCL_X = X_double_bar - A2 * R_bar
UCL_R = D4 * R_bar
LCL_R = D3 * R_bar

# Auswertungsdaten für Excel speichern
auswertung = []

# 📊 X̄-Karte plotten
plt.figure(figsize=(12, 6))
plt.plot(X_bar, marker="o", linestyle="-", label="X̄-Werte")
plt.axhline(UCL_X, color="red", linestyle="dashed", label="UCL")
plt.axhline(LCL_X, color="red", linestyle="dashed", label="LCL")
plt.axhline(X_double_bar, color="blue", linestyle="dotted", label="Mittelwert")
plt.legend()
plt.title("X̄-Karte mit Nelson-Regeln")
plt.xlabel("Stichprobe")
plt.ylabel("X̄-Wert")

# 📌 Nelson-Regeln für X̄-Karte prüfen und auswerten
for i in range(n):
    # Erstellen einer Zeile für jede Stichprobe
    auswertung_zeile = [i+1, X_bar[i], R[i]]

    # Regel: Punkt außerhalb der UCL oder LCL (X̄)
    rule_1_X = "Ja" if X_bar[i] > UCL_X or X_bar[i] < LCL_X else "Nein"

    # Regel: 9 aufeinanderfolgende Punkte auf einer Seite des Mittelwerts (X̄)
    rule_2_X = "Ja" if i >= 8 and (all(X_bar[i-8:i+1] > X_double_bar) or all(X_bar[i-8:i+1] < X_double_bar)) else "Nein"

    # 3️⃣ Regel: 6 aufeinanderfolgende Punkte steigen oder fallen (X̄)
    rule_3_X = "Ja" if i >= 5 and (all(X_bar[j] < X_bar[j+1] for j in range(i-5, i)) or all(X_bar[j] > X_bar[j+1] for j in range(i-5, i))) else "Nein"

    # 4️⃣ Regel: 14 aufeinanderfolgende Punkte wechseln (Zick-Zack, X̄)
    rule_4_X = "Ja" if i >= 14 and all((X_bar[j] > X_bar[j-1] and X_bar[j] < X_bar[j+1]) or (X_bar[j] < X_bar[j-1] and X_bar[j] > X_bar[j+1]) for j in range(i-13, i)) else "Nein"

    # 1️⃣ Regel: Punkt außerhalb der UCL oder LCL (R)
    rule_1_R = "Ja" if R[i] > UCL_R or R[i] < LCL_R else "Nein"

    # 2️⃣ Regel: 9 aufeinanderfolgende Punkte auf einer Seite des Mittelwerts (R)
    rule_2_R = "Ja" if i >= 8 and (all(R[i-8:i+1] > R_bar) or all(R[i-8:i+1] < R_bar)) else "Nein"

    # 3️⃣ Regel: 6 aufeinanderfolgende Punkte steigen oder fallen (R)
    rule_3_R = "Ja" if i >= 5 and (all(R[j] < R[j+1] for j in range(i-5, i)) or all(R[j] > R[j+1] for j in range(i-5, i))) else "Nein"

    # 4️⃣ Regel: 14 aufeinanderfolgende Punkte wechseln (Zick-Zack, R)
    rule_4_R = "Ja" if i >= 14 and all((R[j] > R[j-1] and R[j] < R[j+1]) or (R[j] < R[j-1] and R[j] > R[j+1]) for j in range(i-13, i)) else "Nein"

    # Hinzufügen der Ergebnisse zur Auswertungs-Liste
    auswertung_zeile.extend([rule_1_X, rule_2_X, rule_3_X, rule_4_X, rule_1_R, rule_2_R, rule_3_R, rule_4_R])
    auswertung.append(auswertung_zeile)

# 🔄 Umwandeln der Auswertungsdaten in ein DataFrame
columns = [
    "Stichprobe", "X̄-Wert", "R-Wert", 
    "Regel 1 (X̄)", "Regel 2 (X̄)", "Regel 3 (X̄)", "Regel 4 (X̄)", 
    "Regel 1 (R)", "Regel 2 (R)", "Regel 3 (R)", "Regel 4 (R)"
]
df_auswertung = pd.DataFrame(auswertung, columns=columns)

# 💾 Auswertung in eine Excel-Datei speichern
df_auswertung.to_excel(auswertungsatei, index=False)

# 📊 R-Karte plotten
plt.figure(figsize=(12, 6))
plt.plot(R, marker="o", linestyle="-", label="R-Werte")
plt.axhline(UCL_R, color="red", linestyle="dashed", label="UCL")
plt.axhline(LCL_R, color="red", linestyle="dashed", label="LCL")
plt.axhline(R_bar, color="blue", linestyle="dotted", label="Mittelwert")
plt.legend()
plt.title("R-Karte mit Nelson-Regeln")
plt.xlabel("Stichprobe")
plt.ylabel("R-Wert")
plt.show()
