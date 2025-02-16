import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split

# Beispieldaten (Einkommen, Kreditwürdigkeit, Kreditkarte genehmigt?)
data = {
    "Einkommen": [40, 60, 30, 80, 70, 20, 90, 50],
    "Kreditwürdigkeit": [0, 1, 0, 1, 1, 0, 1, 0],  # 0 = schlecht, 1 = gut
    "Genehmigt": [0, 1, 0, 1, 1, 0, 1, 0]  # 0 = Nein, 1 = Ja
}

# DataFrame erstellen
df = pd.DataFrame(data)

# Eingangsvariablen (X) und Zielvariable (y) definieren
X = df[["Einkommen", "Kreditwürdigkeit"]]
y = df["Genehmigt"]

# Daten in Trainings- und Testset aufteilen
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entscheidungsbaum-Classifier erstellen
tree = DecisionTreeClassifier(criterion="gini", max_depth=3, random_state=42)
tree.fit(X_train, y_train)

# Baumstruktur ausgeben
tree_rules = export_text(tree, feature_names=list(X.columns))
print(tree_rules)

# Vorhersage für einen neuen Kunden (z. B. Einkommen = 65, Kreditwürdigkeit = 1)
neuer_kunde = np.array([[65, 1]])
vorhersage = tree.predict(neuer_kunde)
print(f"Kreditkarte genehmigt: {'Ja' if vorhersage[0] == 1 else 'Nein'}")
