import networkx as nx
from typing import Any, List, Union


def dpath(
    G: nx.Graph,
    source: Union[int, str],
    target: Union[int, str],
    weight: str = "weight",
) -> List[Any]:
    return nx.dijkstra_path(G,)
