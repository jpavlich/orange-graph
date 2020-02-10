import networkx as nx
from inspect import getmembers, isfunction, getargspec

for m in getmembers(nx):
    if isfunction(m[1]):
        print(m[0])
        print(getargspec(m[1]))

# nx.all_neighbors
