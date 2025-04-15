import networkx as nx
import json

# Graph erstellen
G = nx.Graph()

# Knoten (Personen oder Firmen) hinzufügen
G.add_node("Alice", type="Person")
G.add_node("Bob", type="Person")
G.add_node("FirmaX", type="Firma")
G.add_node("FirmaY", type="Firma")

# Kanten (Beziehungen) hinzufügen
# Kanten haben hier zusätzliche Attribute wie "Beziehung" (z.B. "Vorstandsmitglied von")
G.add_edge("Alice", "FirmaX", Beziehung="Vorstandsmitglied von")
G.add_edge("Bob", "FirmaX", Beziehung="Vorstandsmitglied von")
G.add_edge("Alice", "FirmaY", Beziehung="Hat Kredit von")
G.add_edge("Bob", "FirmaY", Beziehung="Hat Kredit von")

# Graph als JSON speichern
graph_data = nx.node_link_data(G)  # Wandelt Graph in JSON-Format um
with open("graph.json", "w") as f:
    json.dump(graph_data, f, indent=4)

print("Graph gespeichert als graph.json")
