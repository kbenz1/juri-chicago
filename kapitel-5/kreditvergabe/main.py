import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from graphviz import Digraph
import pickle

# 1. Excel laden
df = pd.read_excel("kreditnehmerinnen.xlsx")
features = ['Umsatz', 'Vermögen', 'Gold', 'Immobilien']
target = 'Gruppe'

# 2. Diskretisierung + Schwellen speichern
bin_edges = {}  # hier speichern wir die echten Schwellen pro Feature
for feat in features:
    qcut, bins = pd.qcut(df[feat], 3, labels=[0, 1, 2], retbins=True, duplicates='drop')
    df[feat + '_cat'] = qcut.astype(int)
    bin_edges[feat] = bins  # enthält z. B. [10000.0, 20000.0, 40000.0, 80000.0]

X = df[[f + '_cat' for f in features]]
y = df[target]

# 3. Trainieren
clf = DecisionTreeClassifier(criterion='entropy', max_depth=4, random_state=42)
clf.fit(X, y)

# 4. Farben
class_colors = {
    'A': '#cce5ff',
    'B': '#ffe5cc',
    'C': '#f7ccf7',
}

# 5. Feature-Mapping
feature_cat_names = [f + '_cat' for f in features]
feature_mapping = dict(zip(feature_cat_names, features))

dot = Digraph()
dot.attr('node', shape='box', style='filled', fontname='Helvetica')

# 6. Baum aufbauen
def add_nodes(dot, node_id):
    left_id = clf.tree_.children_left[node_id]
    right_id = clf.tree_.children_right[node_id]
    is_leaf = left_id == -1 and right_id == -1

    if is_leaf:
        class_index = clf.tree_.value[node_id][0].argmax()
        class_label = clf.classes_[class_index]
        color = class_colors.get(class_label, "#dddddd")
        dot.node(str(node_id), label=class_label, fillcolor=color)
        return class_label

    # Prüfen: Sind beide Kinder Blätter?
    left_is_leaf = clf.tree_.children_left[left_id] == -1 and clf.tree_.children_right[left_id] == -1
    right_is_leaf = clf.tree_.children_left[right_id] == -1 and clf.tree_.children_right[right_id] == -1

    if left_is_leaf and right_is_leaf:
        left_class = clf.classes_[clf.tree_.value[left_id][0].argmax()]
        right_class = clf.classes_[clf.tree_.value[right_id][0].argmax()]

        # Pfadrichtung anpassen: nein führt zu „schlechterer“ Klasse
        if right_class > left_class:
            left_id, right_id = right_id, left_id
            left_class, right_class = right_class, left_class

        if left_class == right_class:
            color = class_colors.get(left_class, "#dddddd")
            dot.node(str(node_id), label=left_class, fillcolor=color)
            return left_class

    # Normale Knotenlogik mit originalem Schwellenwert
    feature_idx = clf.tree_.feature[node_id]
    threshold = clf.tree_.threshold[node_id]

    feature_cat = feature_cat_names[feature_idx]
    original_feature = feature_mapping[feature_cat]
    bins = bin_edges[original_feature]

    bin_index = int(threshold + 0.5)
    if bin_index >= len(bins):
        real_threshold = bins[-1]
    else:
        real_threshold = bins[bin_index]

    if original_feature == "Gold":
        label = f"{original_feature}\n≤ {real_threshold:,.0f} oz."
    else:
        label = f"{original_feature}\n≤ {real_threshold:,.0f} €"

    dot.node(str(node_id), label=label, fillcolor="#b3e6b3")

    left_class = add_nodes(dot, left_id)
    right_class = add_nodes(dot, right_id)

    dot.edge(str(node_id), str(left_id), label="ja")
    dot.edge(str(node_id), str(right_id), label="nein")

    return None



# 7. Baum starten
add_nodes(dot, 0)
dot.render("entscheidungsbaum", format="png", cleanup=False)
dot.view()

# 8. Entscheidungsbaum speichern (für spätere Klassifikation)
with open("baummodell.pkl", "wb") as f:
    pickle.dump(clf, f)
dot.save("entscheidungsbaum.dot")
