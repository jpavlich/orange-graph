import networkx as nx
from networkx.algorithms.approximation.clique import max_clique

G = nx.DiGraph()
for i in range(0, 10):
    G.add_node(i)

for i in range(0, 10):
    for j in range(0, 10):
        G.add_edge(i, j)

mclique: set = max_clique(G)

print(mclique)
