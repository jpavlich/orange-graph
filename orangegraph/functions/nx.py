import networkx as nx
from typing import List
from util.orange_decorators import orange_meta


@orange_meta()
def dpath(
    G: nx.Graph, source: object, target: object, weight: str = "weight",
) -> List[object]:
    return nx.dijkstra_path(G, source, target, weight)
